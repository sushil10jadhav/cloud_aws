import boto3
session=boto3.session.Session(profile_name="DevAdmin")
ec2_con=session.client(service_name="ec2")

#Retrieve all region/endpoints that work with ec2
response=ec2_con.describe_regions()
#print response

#Retrieve availability zone for region on ec2 objects
res=ec2_con.describe_availability_zones()
print("Availabilityzone=",res['AvailabilityZones'])
