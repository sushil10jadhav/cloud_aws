#instance id = i-011e9629baf9d7c3c
import boto3 
session=boto3.session.Session(profile_name="DevAdmin")
ec2_con=session.resource(service_name="ec2",region_name="us-east-1")
my_inst=ec2_con.Instance(id="i-011e9629baf9d7c3c")
print dir(my_inst)
#my_inst.start()
#my_inst.stop()
#print my_inst.state['Name']
