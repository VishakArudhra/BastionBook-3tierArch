# originally hosted on lambda function and fronted with an API Gateway as guided in
# the below user guide: https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html
import boto3
from flask import (
    Flask, request, render_template, redirect, url_for, flash
)
import json
from markupsafe import escape
import re
import requests

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def handler():
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''
    
    if request.method == 'POST':

        # define the DynamoDB table that Lambda will connect to
        tableName = "lambda-apigateway"

        # create the DynamoDB resource
        dynamo = boto3.resource('dynamodb', region_name="us-west-2").Table(tableName)

        # define the functions used to perform the CRUD operations
        def ddb_create(x):
            return dynamo.put_item(**x)

        def ddb_read(x):
            return dynamo.get_item(**x)
        
        def ddb_getall():
            data = dynamo.scan()
            return data["Items"]

        def ddb_update(x):
            return dynamo.update_item(**x)
            
        def ddb_delete(x):
            return dynamo.delete_item(**x)

        def echo(x):
            return x
        

        content = request.get_json()

        operation = content['operation']


        operations = {
            'create': ddb_create,
            'read': ddb_read,
            'update': ddb_update,
            'delete': ddb_delete,
            'getall': ddb_getall,
            'echo': echo,
        }

        if operation in operations:
            if operation == 'getall':
                return operations[operation]()
            return operations[operation](content.get('payload'))
        else:
            raise ValueError('Unrecognized operation "{}"'.format(operation))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
