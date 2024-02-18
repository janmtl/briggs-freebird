import os
import boto3

def get_timestream_client():
    AWS_ACCESS_KEY_ID = os.environ['FREEBIRD_AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['FREEBIRD_AWS_SECRET_ACCESS_KEY']
    REGION_NAME = os.environ['FREEBIRD_REGION_NAME']
    session = (
        boto3
        .Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME
        )
    )
    timestream_query_client = session.client('timestream-query')
    return timestream_query_client