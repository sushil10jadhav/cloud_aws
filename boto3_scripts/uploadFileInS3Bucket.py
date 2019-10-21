import boto3
session=boto3.session.Session(profile_name="DevAdmin")
s3_col_cli=session.client(service_name="s3",region_name="us-east-1")
fileName='testF2.txt'
bucketName='sushil.aws.asociate101919'
s3_col_cli.upload_file(fileName,bucketName,'testFile3.txt')