import pandas as pd

def timestream_query_to_dataframe(client, QueryString):
    timestream_response = client.query(
        QueryString=QueryString,
        MaxRows=1000
    )
    rows = timestream_response['Rows']
    column_names = timestream_response['ColumnInfo']
    output_frame = (
        pd
        .DataFrame([
            {
                col['Name']: val['ScalarValue']
                for col, val in zip(column_names, row['Data'])
            }
            for row in rows
        ])
    )
    return output_frame