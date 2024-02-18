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

for root, dirs, files in os.walk(local_directory):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, local_directory)
        s3_path = os.path.join('/', relative_path)
        s3_client.upload_file(local_path, BUCKET_NAME, s3_path)
