import sys

import pandas as pd

from utils.get_timestream_client import get_timestream_client
from utils.timestream_to_dataframe import timestream_query_to_dataframe

QueryString = (
    open('docs/data/queries/detectionsByDayL365.sql')
    .read()
    .replace('${TOP_K}', '8')
)
timestream_query_client = get_timestream_client()

results0 = timestream_query_to_dataframe(
    client=timestream_query_client,
    QueryString=QueryString
)

output_frame0 = (
    results0
    .pipe(lambda x: x.assign(time=pd.to_datetime(x['time'])))
    .pipe(lambda x: x[x['time'] >= pd.Timestamp('2024-02-01')])
    .pipe(lambda x: x.assign(time=x['time'].dt.strftime("%Y-%m-%d")))
    .pipe(lambda x: x.assign(detections_cnt=x['detections_cnt'].astype(int)))
)

output_frame0.to_csv(sys.stdout, index=False)