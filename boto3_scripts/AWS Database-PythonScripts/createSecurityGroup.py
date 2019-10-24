import boto3
import json
import datetime

session=boto3.session.Session(profile_name="DevAdmin")
ec2_cons=session.client(service_name="ec2",region_name="us-east-1")
sg_name="rds_sg_dev"
sg_description="RDS Security Group for AWS Dev Study"
my_ip_cidr="0.0.0.0/0"   # Or better use your own ip -
response=ec2_cons.create_security_group (
    Description=sg_description,
    GroupName=sg_name
    )
print(json.dumps(response,indent=2,sort_keys=True))

#Rule for security group:--
response=ec2_cons.authorize_security_group_ingress(
        CidrIp=my_ip_cidr,
        FromPort=3306,
        GroupName=sg_name,
        ToPort=3306,
        IpProtocol='tcp'
    )
print("Security group should be created ! Verify the same in AWS Console")
