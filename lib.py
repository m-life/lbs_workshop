import os
import boto3
from dotenv import load_dotenv

load_dotenv('dev.env')


def get_client(service):
    session = boto3.session.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )
    return session.client(service, region_name='eu-west-1')


def upload_file(file_name, bucket, object_name):
    s3_client = get_client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    print(f'Uploaded {file_name} to s3://{bucket}/{object_name}')
    return response


def list_files(bucket_name):
    s3_client = get_client('s3')

    # Initialize paginator to handle buckets with many objects
    paginator = s3_client.get_paginator('list_objects_v2')

    # List objects within the bucket using the paginator
    page_iterator = paginator.paginate(Bucket=bucket_name)

    # Collect all files excluding folders
    files = []
    for page in page_iterator:
        for obj in page.get('Contents', []):  # Ensure there are contents
            key = obj['Key']
            if not key.endswith('/'):  # Exclude folders
                files.append(key)

    return files


def generate_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string, name of the bucket.
    :param object_name: string, name of the object.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :return: Presigned URL as string. If error, returns None.
    """
    # Create a s3 client
    s3_client = boto3.client('s3')

    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration)
