import boto3
session=boto3.session.Session(profile_name="DevAdmin")
ec2_col=session.client(service_name="ec2",region_name="us-east-1")
ec2_col.delete_key_pair(KeyName="MyKeyvaiBoto")
print(ec2_col)