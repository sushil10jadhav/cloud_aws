import boto3
import json
import datetime

def dropDBInstance(rdsId):
    try:
        
        rds_identifier=rdsId
        session=boto3.session.Session(profile_name="DevAdmin")
        rds_client=session.client(service_name="rds",region_name="us-east-1")
        
        response=rds_client.delete_db_instance(DBInstanceIdentifier=rds_identifier,SkipFinalSnapshot=True)
        print ("RDS Instance is being droped , which may take 10-20 mins")
        waiter=rds_client.get_waiter('db_instance_deleted')
        waiter.wait(DBInstanceIdentifier=rds_identifier)

        print("RDS database is droped now cleaning up security group")
        
        # Now clean up security group rds_sg_dev --
        ec2_cons=session.client(service_name="ec2",region_name="us-east-1")
        sg_name="rds_sg_dev"

        response=ec2_cons.describe_security_groups(
            GroupNames=[
                sg_name
            ])
        sg_id_number=json.dumps(response['SecurityGroups'][0]['GroupId'])
        sg_id_number=sg_id_number.replace('"','')
        print ("Starting clean up for security group :" + sg_id_number)
        
        response=ec2_cons.delete_security_group(GroupId=sg_id_number)
        
        print ("Clean up completed!!!")

    except Exception as e:
        print (e.message)        
        raise e

def main():
    print ("Python program to drop db instnace and delete security group")
    dropDBInstance('nypsummit')
    print ("Success")

if __name__== '__main__':
    main()

