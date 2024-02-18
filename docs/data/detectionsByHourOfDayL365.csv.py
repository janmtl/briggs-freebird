import sys

import pandas as pd

from utils.get_timestream_client import get_timestream_client
from utils.timestream_to_dataframe import timestream_query_to_dataframe

QueryString = (
    open('docs/data/queries/detectionsByHourOfDayL365.sql')
    .read()
)
timestream_query_client = get_timestream_client()

results0 = timestream_query_to_dataframe(
    client=timestream_query_client,
    QueryString=QueryString
)

output_frame0 = (
    results0
    .pipe(lambda x: x.assign(detections_cnt=x['detections_cnt'].astype(int)))
    .pipe(lambda left: pd.merge(
        left,
        left.groupby('sciName')['detections_cnt'].sum().rename('total_detections_cnt').reset_index(),
        how='left'
    ))
    .pipe(lambda x: x[x['total_detections_cnt'] >= 10])
    .pipe(lambda x: x.assign(hour_of_day=x['hour_of_day'].astype(int)))
)

output_frame0.to_csv(sys.stdout, index=False)