import boto3
session=boto3.session.Session(profile_name="DevAdmin")
ec2_con=session.client(service_name="ec2",region_name="us-east-1")
key=ec2_con.create_key_pair(KeyName="MyKeyvaiBoto")
print(key)