import boto3
import json
import datetime

def date_time_conversion(o):
    if isinstance(o,datetime.datetime):
        return o.__str__()

def createDynamoDbTable(tableToCreate):
    try:
        tableName=tableToCreate
        session=boto3.session.Session(profile_name="DevAdmin")
        dynamodb_client=session.client(service_name="dynamodb",region_name="us-east-1")
        table=dynamodb_client.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName':'User_Id',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'User_Email',
                    'KeyType':'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName':'User_Id',
                    'AttributeType':'S'
                },
                {
                    'AttributeName':'User_Email',
                    'AttributeType':'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }        
        )
        print ("Dynamodb table is being created, this may take 2-5 minutes!!")
        
        waiter=dynamodb_client.get_waiter('table_exists')
        waiter.wait(TableName=tableName)

        print ("Table " + tableName + " is ready!!")
    except Exception as e:
        raise e

def main():
    print ("Python program to create Dynamodb table !!")
    createDynamoDbTable('Users')
    print ("Success!!")

if __name__== '__main__':
    main()