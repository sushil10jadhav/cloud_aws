import boto3
import json
import datetime
import botocore

# Print datetime in raw JSON format 
def date_time_converter(o):
    if isinstance(o,datetime.datetime):
        return o.__str__()

#Variable 
sg_name='rds_sg_dev'
rdsidentifier='NYPSUMMIT'  #'yourDBID'
db_name='mytestdb'
user_name='mastersushil'
user_password='masterpassw0rd1!'
amdin_email='sample@gmail.com'
sg_id_number=''
rds_endpoint=''

session=boto3.session.Session(profile_name="DevAdmin")
ec2_client=session.client(service_name="ec2",region_name="us-east-1")
response=ec2_client.describe_security_groups(
    GroupNames=[
        sg_name
    ])
sg_id_number=json.dumps(response['SecurityGroups'][0]['GroupId'])
sg_id_number=sg_id_number.replace('"','')

print("Security Group Id :=",sg_id_number)

#RDS Client--
#rds_client=session.client(service_name="rds",region_name="us-east-1")

#session1=boto3.session.Session(profile_name="DevAdmin")
rds_client=session.client(service_name="rds",region_name="us-east-1")
#rds_client=session1.client(service_name='rds',region_name='us-east-1')

try:
    response=rds_client.create_db_instance(
        DBName=db_name,
        DBInstanceIdentifier=rdsidentifier,
        DBInstanceClass='db.t2.micro',
        Engine='mariadb',
        MasterUsername=user_name,
        MasterUserPassword=user_password,
        VpcSecurityGroupIds=[
            sg_id_number
        ],
        AllocatedStorage=20,
        Tags=[
            {
                'Key':'POC-Email',
                'Value':amdin_email

            },
            {
                'Key':'Purpose',
                'Value':'AWS Developer Exam Practice'            
            }
        ]
    )
    #Wait until the db instance is created so use waiter-->
    print ('Creating RDS instacen , which may take 10-20 mins')
    waiter=rds_client.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=rdsidentifier)
    print ('Good!! RDS instnace is up now!')
except botocore.exceptions.ClientError as e:
    if 'DBInstanceAlreadyExists' in e.message:
        print 'DB Instance %s exists already ,continue to poll...' %rdsidentifier 
    else:
        raise

"""
running = True
    while running:
        response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)

        db_instances = response['DBInstances']
        if len(db_instances) != 1:
            raise Exception('Whoa cowboy! More than one DB instance returned; this should never happen')

        db_instance = db_instances[0]

        status = db_instance['DBInstanceStatus']

        print 'Last DB status: %s' % status

        time.sleep(5)
        if status == 'available':
            endpoint = db_instance['Endpoint']
            host = endpoint['Address']
            # port = endpoint['Port']

            print 'DB instance ready with host: %s' % host
            running = False


if __name__ == '__main__':
    main()
"""
print "Very good Learning!!!"    