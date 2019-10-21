import boto3
session =boto3.session.Session(profile_name="DevAdmin")
s3_con_cli=session.client(service_name="s3",region_name="us-east-1")
s3_con_cli.create_bucket(Bucket="sushil.aws.asociate101919")
