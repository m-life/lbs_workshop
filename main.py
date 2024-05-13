import os
import boto3
from dotenv import load_dotenv

load_dotenv('dev.env')


def get_s3_client():
    session = boto3.session.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )
    return session.client('s3', region_name='eu-west-1')


def upload_file(file_name, bucket, object_name):
    s3_client = get_s3_client()
    response = s3_client.upload_file(file_name, bucket, object_name)
    print(f'Uploaded {file_name} to s3://{bucket}/{object_name}')
    return response
