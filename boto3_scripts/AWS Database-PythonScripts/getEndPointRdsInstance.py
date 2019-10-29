import boto3
import json
import datetime
#import botocore

# Helper function to convert datetime conversion:
def date_time_conversion(o):
    if isinstance(o,datetime.datetime):
        return o.__str__()

def getRdsEndPoint(rdsId):
    #Variables :-
    rds_identifier=rdsId

    try:
        session=boto3.session.Session(profile_name="DevAdmin")
        rds_client=session.client(service_name="rds",region_name="us-east-1")

        print("Fetching RDS Endpoint for ",rds_identifier)
        response=rds_client.describe_db_instances(
            DBInstanceIdentifier=rds_identifier
        )
        rds_endpoint=json.dumps(response['DBInstances'][0]['Endpoint']['Address'])
        rds_endpoint=rds_endpoint.replace('"','')
        print('RDS Endpoint:'+ rds_endpoint )
    #except botocore.exceptions.ClientError as e:
    except Exception as e:
        print ("Error while fetching RDS Endpoint",e.message)
        raise e

def main():
    print ("Python program to get rds endpoint")
    getRdsEndPoint('nypsummit')
    print ("Success")

if __name__== '__main__':
    main()