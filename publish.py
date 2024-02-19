import os

import boto3


AWS_ACCESS_KEY_ID = os.environ['FREEBIRD_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['FREEBIRD_AWS_SECRET_ACCESS_KEY']
REGION_NAME = os.environ['FREEBIRD_REGION_NAME']
BUCKET_NAME = os.environ['FREEBIRD_WWW_BUCKET_NAME']
session = (
    boto3
    .Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )
)
s3_client = session.client('s3')

local_directory = 'dist'

MIME_MAP = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.csv': 'text/csv'
}

for root, dirs, files in os.walk(local_directory):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, local_directory)
        s3_path = relative_path

        file_extension = os.path.splitext(local_path)[-1]
        print(local_path, file_extension, MIME_MAP[file_extension])
        response = s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=relative_path,
            Body=open(local_path, 'rb'),
            ContentType=MIME_MAP[file_extension]
        )
        print(response)