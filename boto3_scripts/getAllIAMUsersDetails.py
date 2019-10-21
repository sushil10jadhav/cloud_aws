import boto3
session=boto3.session.Session(profile_name="DevAdmin")
iam_cli=session.client(service_name="iam",region_name="us-east-1")
for each_user in iam_cli.list_users()['Users']:
    print each_user['UserName'],each_user['Arn']
    #print dir(each_user)
