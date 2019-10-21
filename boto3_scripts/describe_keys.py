import boto3
session=boto3.session.Session(profile_name="DevAdmin")
ec2_con=session.client(service_name="ec2",region_name="us-east-1")
my_key=ec2_con.describe_key_pairs()
#print dir(my_key)
print my_key
print type(my_key)
#print my_key['KeyName']