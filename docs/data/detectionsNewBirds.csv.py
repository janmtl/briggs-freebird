import sys

import pandas as pd

from utils.get_timestream_client import get_timestream_client
from utils.timestream_to_dataframe import timestream_query_to_dataframe
from utils.bird_image_store import load_store, get_image, resize_image, put_image

QueryString = (
    open('docs/data/queries/detectionsNewBirds.sql')
    .read()
)
timestream_query_client = get_timestream_client()

results0 = timestream_query_to_dataframe(
    client=timestream_query_client,
    QueryString=QueryString
)

output_frame0 = (
    results0
    .pipe(lambda x: x.assign(first_time_detected=pd.to_datetime(x['first_time_detected'])))
    .pipe(lambda x: x.assign(first_time_detected=x['first_time_detected'].dt.strftime("%Y-%m-%dT%H:%M:%S")))
)

stored_birds = set(load_store())
all_birds = set(output_frame0["sciName"].values)
new_birds = list(all_birds - stored_birds)
for new_bird in new_birds:
    image = get_image(new_bird)
    put_image(image, new_bird)

output_frame0.to_csv(sys.stdout, index=False)