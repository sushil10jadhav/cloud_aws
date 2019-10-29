import boto3
import json
import datetime
#import pymysql as mariadb       # if error for import :- pip install pymysql
import mysql.connector as mariadb
## ---this script is ahving some issue need to fix --- ""
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

        #print("Fetching RDS Endpoint for ",rds_identifier)
        response=rds_client.describe_db_instances(
            DBInstanceIdentifier=rds_identifier
        )
        rds_endpoint=json.dumps(response['DBInstances'][0]['Endpoint']['Address'])
        rds_endpoint=rds_endpoint.replace('"','')
        #print('RDS Endpoint:'+ rds_endpoint )
        return rds_endpoint
    except Exception as e:
        print ("Error while fetching RDS Endpoint",e.message)
        raise e


def createTable(rdsId):
    try:
        rds_identifier=rdsId
        session=boto3.session.Session(profile_name="DevAdmin")
        rds_client=session.client(service_name="rds",region_name="us-east-1")
        db_name='mytestdb'
        user_name='mastersushil'
        user_password='masterpassw0rd1!'
        amdin_email='sample@gmail.com'

        rds_Endpoint_URL = getRdsEndPoint(rdsId)
        print('RDS Endpoint:'+ rds_Endpoint_URL )

        #Step-1 connect db to create table:
        db_connection=mariadb.connect(host=rds_Endpoint_URL,user=user_name,password=user_password,database=db_name)
        cursor=db_connection.cursor()
        try:
            cursor.excecute("CREATE TABLE Users (user_id INT NOT NULL AUTO_INCREMENT, \
            user_fname VARCHAR(100) NOT NULL,user_lname VARCHAR(100) NOT NULL,\
            user_email varchar(175) not null, PRIMARY KEY(`user_id`))")       
            print "Table created!"
        except mariadb.Error as e:
            print ('Error: {}'.format(e))
        finally:
            db_connection.close()

    except Exception as e:
        print ("Error" ,e.message)
        raise e

    """
        #Step-2 :Insert rows in table-
        db_connection=mariadb.connect(host=rds_Endpoint_URL,user=user_name,password=user_password,database=db_name)
        cursor=db_connection.cursor()
        try:
            sql="INSERT INTO `Users` (`user_fname`,`user_lname`,`user_email`) VALUES(%s,%s,%s)"
            cursor.excecute(sql,('CJ','Smith','casy.smith@example.com'))
            cursor.excecute(sql,('Valmik','Pote','valmik.pote@cognizent.com'))
            cursor.excecute(sql,('Sandy','Shedge','sandesh.shedge@hsbc.com'))
            #No data saved unless transaction is commited!---
            db_connection.commit()
            print ("Inserted data into table")
        except mariadb.Error as e:
            print ('Error: {}'.format(e))
            print ('Something went wrong!!')
        finally:
            db_connection.close()
    """
    
def main():
    print ("Python program to create SQL table in mariadb")
    createTable('nypsummit')
    print ("Success")

if __name__== '__main__':
    main()