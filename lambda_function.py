{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww28600\viewh18000\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import json\
import boto3\
from decimal import Decimal\
\
dynamodb = boto3.resource('dynamodb')\
table = dynamodb.Table('StudentRecords')\
\
def lambda_handler(event, context):\
    # Detect the HTTP method from the event\
    http_method = event.get('httpMethod', '')\
\
    if http_method == 'POST':\
        return create_student(event)\
    elif http_method == 'GET':\
        return get_student(event)\
    elif http_method == 'PUT':\
        return update_student(event)\
    elif http_method == 'DELETE':\
        return delete_student(event)\
    else:\
        return \{\
            'statusCode': 400,\
            'body': json.dumps('Invalid HTTP method')\
        \}\
\
def create_student(event):\
    try:\
        # Parse the student data from the event body\
        student = json.loads(event['body'])\
        # Put the item in DynamoDB\
        table.put_item(Item=student)\
        return \{\
            'statusCode': 200,\
            'body': json.dumps(f"Student \{student['student_id']\} created successfully.")\
        \}\
    except Exception as e:\
        return \{\
            'statusCode': 500,\
            'body': json.dumps(f"Failed to create student: \{str(e)\}")\
        \}\
\
def convert_decimal(obj):\
    """Convert Decimal to float."""\
    if isinstance(obj, Decimal):\
        return float(obj)\
    raise TypeError("Object of type Decimal is not JSON serializable")\
\
def get_student(event):\
    try:\
        # Get student_id from queryStringParameters\
        student_id = event['queryStringParameters']['student_id']\
        response = table.get_item(Key=\{'student_id': student_id\})\
\
        if 'Item' in response:\
            student = response['Item']\
            return \{\
                'statusCode': 200,\
                'body': json.dumps(student, default=convert_decimal)\
            \}\
        else:\
            return \{\
                'statusCode': 404,\
                'body': json.dumps(f"Student with ID \{student_id\} not found")\
            \}\
    except Exception as e:\
        return \{\
            'statusCode': 500,\
            'body': json.dumps(f"Error fetching student: \{str(e)\}")\
        \}\
        \
def update_student(event):\
    try:\
        student = json.loads(event['body'])\
        student_id = student['student_id']\
        \
        # Update item in DynamoDB\
        response = table.update_item(\
            Key=\{'student_id': student_id\},\
            UpdateExpression="set #name = :name, age = :age, major = :major",\
            ExpressionAttributeNames=\{\
                '#name': 'name'\
            \},\
            ExpressionAttributeValues=\{\
                ':name': student.get('name'),\
                ':age': student.get('age'),\
                ':major': student.get('major')\
            \},\
            ReturnValues="UPDATED_NEW"\
        )\
        \
        return \{\
            'statusCode': 200,\
            'body': json.dumps(f"Student \{student_id\} updated successfully.")\
        \}\
    except Exception as e:\
        return \{\
            'statusCode': 500,\
            'body': json.dumps(f"Failed to update student: \{str(e)\}")\
        \}\
\
def delete_student(event):\
    try:\
        student_id = event['queryStringParameters']['student_id']\
        \
        # Delete item from DynamoDB\
        response = table.delete_item(\
            Key=\{'student_id': student_id\}\
        )\
        \
        return \{\
            'statusCode': 200,\
            'body': json.dumps(f"Student \{student_id\} deleted successfully.")\
        \}\
    except Exception as e:\
        return \{\
            'statusCode': 500,\
            'body': json.dumps(f"Failed to delete student: \{str(e)\}")\
        \}\
\
# Define update_student and delete_student similarly\
}