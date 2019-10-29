import boto3
import json
import datetime
#import pymysql as mariadb       # if error for import :- pip install pymysql
#import pymysql.cursors
import mysql.connector as mariadb


#import mysql.connector as mariadb

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
        try:
            db_connection=mariadb.connect(host=rds_Endpoint_URL,user=user_name,password=user_password,database=db_name)
            cursor=db_connection.cursor()
            #cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
            
            cursor.execute("CREATE TABLE Users1 (user_id INT NOT NULL AUTO_INCREMENT,\
            user_fname VARCHAR(100) NOT NULL,user_lname VARCHAR(100) NOT NULL, \
            user_email varchar(175) not null, PRIMARY KEY(`user_id`))")       

            print ("Table created!")

            """
            cursor.execute("SELECT VERSION()")
            query_result=cursor.fetchall()
            print ("Query Result:=")
            print (query_result)            
            """
            
            """
            cursor.execute("SHOW TABLES")
            for x in cursor:
                print (x)
            """            
        except mariadb.Error as e:
            print ('Error: {}'.format(e))
        finally:
            db_connection.close()

        #Step-2 :Insert rows in table-
        
        try:
            db_connection=mariadb.connect(host=rds_Endpoint_URL,user=user_name,password=user_password,database=db_name)
            cursor=db_connection.cursor()
            sql="INSERT INTO `Users1` (`user_fname`,`user_lname`,`user_email`) VALUES(%s,%s,%s)"
            cursor.execute(sql,('CJ','Smith','casy.smith@example.com'))
            cursor.execute(sql,('Valmik','Pote','valmik.pote@cognizent.com'))
            cursor.execute(sql,('Sandy','Shedge','sandesh.shedge@hsbc.com'))
            #No data saved unless transaction is commited!---
            db_connection.commit()
            print ("Inserted data into table")

            cursor.execute("SELECT * FROM Users1")
            query_result = cursor.fetchall()
            print ("Querying Users table:- and here is the data in it:-")
            print (query_result)

        except mariadb.Error as e:
            print ('Error: {}'.format(e))
            print ('Something went wrong!!')
        finally:
            db_connection.close()

    except Exception as e:
        #print ("Error" ,e.message)``
        raise e

def main():
    print ("Python program to create SQL table in mariadb")
    createTable('nypsummit')
    print ("Success")

if __name__== '__main__':
    main()