import boto3
import os
from datetime import datetime
import random
import json

s3 = boto3.client('s3', region_name='eu-west-1')



def read_logs_from_s3():

    # Specify the bucket and the key of the object
    bucket_name = 'alexandria-data-staged'
    key = 'ml/trulens/latest_file.json'

    # Get the object
    response = s3.get_object(Bucket=bucket_name, Key=key)
    
    # Get the body of the response
    body = response['Body']

    # Read the body of the response
    data = body.read()

    # Decode the bytes to string
    str_data = data.decode('utf-8')

    # Load the JSON to a Python object
    json_data = json.loads(str_data)

    list_unprocessed_files = []

    list_unprocessed_files = list(filter(lambda x: x["status"] == "open", json_data))

    return list_unprocessed_files


def write_logs_to_s3(list_file_not_processed, status):

    # Specify the bucket and the key of the object
    bucket_name = 'alexandria-data-staged'
    key = 'ml/trulens/latest_file.json'

    for record in list_file_not_processed:
        record['status'] = status
        record['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert the Python object to JSON
    json_str = json.dumps(list_file_not_processed)

    # Upload the file to S3
    # print(json_str)
    # s3.upload_file('latest_file.json', bucket_name, key)
    s3.put_object(Body=json_str, Bucket=bucket_name, Key=key)




def read_text_file_s3(list_unprocessed_files):

    # Specify the bucket and the key of the object
    bucket_name = 'alexandria-data-staged'
    key = 'ml/trulens/'
    
    list_filename_data = []
    for file in list_unprocessed_files:
        file = file["file_name"]
        key_file = os.path.join(key, file)

        # Get the object
        response = s3.get_object(Bucket=bucket_name, Key=key_file)
    
        # Get the body of the response
        body = response['Body']

        # Read the body of the response
        data = body.read()
        data = json.loads(data)

        list_filename_data.extend(data)

    return list_filename_data