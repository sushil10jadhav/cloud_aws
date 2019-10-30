#!/usr/bin/env bash
#
# badfinder.sh
#
# This script finds problematic CloudFormation stacks and EC2 instances in the AWS account/region your credentials point at.
# It finds CF stacks with missing/terminated and stopped EC2 hosts.  It finds EC2 hosts with missing owner and expires tags.
# It finds unattached volumes. Should you delete them all?  Probably. Kill the EC2 instances first because it'll probably
# make more orphan CF stacks.
#

BADSTACKS=""
STOPPEDSTACKS=""

echo "Finding misconfigured AWS assets, stand by..."
for STACK in $(aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --max-items 1000 | jq -r '.StackSummaries[].StackName')
do
        INSTANCE=$(aws cloudformation describe-stack-resources --stack-name $STACK | jq -r '.StackResources[] | select (.ResourceType=="AWS::EC2::Instance")|.PhysicalResourceId')
        if [[ ! -z $INSTANCE  ]]; then
                STATUS=$(aws ec2 describe-instance-status --include-all-instances --instance-ids $INSTANCE 2> /dev/null | jq -r '.InstanceStatuses[].InstanceState.Name') 
                if [[ -z $STATUS  ]]; then
                        BADSTACKS="${BADSTACKS:+$BADSTACKS }$STACK"
                elif [[ ${STATUS} == "stopped" ]]; then
                        STOPPEDSTACKS="${STOPPEDSTACKS:+$STOPPEDSTACKS }$STACK"
            fi
        fi
done

echo "CloudFormation stacks with missing EC2 instances: (aws cloudformation delete-stack --stack-name)"
echo $BADSTACKS

echo "CloudFormation stacks with stopped EC2 instances: (aws cloudformation delete-stack --stack-name)"
echo $STOPPEDSTACKS

echo "EC2 instances without owner tag: (aws ec2 terminate-instances --instance-ids)"
aws ec2 describe-instances --query "Reservations[].Instances[].{ID: InstanceId, Tag: Tags[].Key}" --output json | jq -c '.[]' | grep -vi owner | jq -r '.ID' | awk -v ORS=' ' '{ print $1  }' | sed 's/ $//'

echo "EC2 instances without expires tag: (aws ec2 terminate-instances --instance-ids)"
aws ec2 describe-instances --query "Reservations[].Instances[].{ID: InstanceId, Tag: Tags[].Key}" --output json | jq -c '.[]' | grep -vi expires | jq -r '.ID' | awk -v ORS=' ' '{ print $1   }' | sed 's/ $//'

echo "Unattached EBS volumes: (aws ec2 delete-volume --volume-id)"
aws ec2 describe-volumes --query 'Volumes[?State==`available`].{ID: VolumeId, State: State}' --output json | jq -c '.[]' | jq -r '.ID' | awk -v ORS=' ' '{ print $1  }' | sed 's/ $//'

exit