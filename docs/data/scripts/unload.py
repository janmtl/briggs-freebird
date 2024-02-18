import os
import json
import sys
from urllib.parse import urlparse

import boto3

import pandas as pd

AWS_ACCESS_KEY_ID = os.environ['FREEBIRD_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['FREEBIRD_AWS_SECRET_ACCESS_KEY']
REGION_NAME = os.environ['FREEBIRD_REGION_NAME']
S3_BUCKET_NAME = os.environ['FREEBIRD_S3_BUCKET_NAME']
session = (
    boto3
    .Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )
)
timestream_query_client = session.client('timestream-query')
s3_client = session.client('s3')

QueryString = f"""
UNLOAD (SELECT * FROM freebirdDB."detectionStatsTBL")
TO 's3://{S3_BUCKET_NAME}/detectionstatstbl'
WITH (
  format='CSV',
  include_header='true',
  compression='NONE'
)
"""
timestream_unload_response = timestream_query_client.query(
    QueryString=QueryString,
    MaxRows=1000
)

timestream_unload_manifest_fullpath = timestream_unload_response['Rows'][0]['Data'][2]['ScalarValue']
timestream_unload_manifest_path = urlparse(timestream_unload_manifest_fullpath, allow_fragments=False)
timestream_unload_manifest_bucket = timestream_unload_manifest_path.netloc
timestream_unload_manifest_key = timestream_unload_manifest_path.path[1:]

unload_manifest_object = s3_client.get_object(
    Bucket=timestream_unload_manifest_bucket,
    Key=timestream_unload_manifest_key
)
unload_manifest = json.loads(unload_manifest_object['Body'].read())
unload_manifest

unload_results_fullpath = unload_manifest['result_files'][0]['url']
unload_results_path = urlparse(unload_results_fullpath, allow_fragments=False)
unload_results_bucket = unload_results_path.netloc
unload_results_key = unload_results_path.path[1:]
unload_results_object = s3_client.get_object(
    Bucket=unload_results_bucket,
    Key=unload_results_key
)
input_frame = pd.read_csv(unload_results_object['Body'])