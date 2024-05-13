import boto3
from config import Settings


def get_client(service: str, settings: Settings):
    session = boto3.session.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
    )
    return session.client(service, region_name='eu-west-1')


def list_files(s3_client, bucket_name):
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    files = []
    for page in page_iterator:
        for obj in page.get('Contents', []):  # Ensure there are contents
            key = obj['Key']
            if not key.endswith('/'):  # Exclude folders
                files.append(key)

    return files