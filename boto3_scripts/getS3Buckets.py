import boto3
session=boto3.session.Session(profile_name="DevAdmin")
s3_con_cli=session.client(service_name="s3",region_name="us-east-1")
for each_bucket in s3_con_cli.list_buckets()['Buckets']:
    print each_bucket['Name']