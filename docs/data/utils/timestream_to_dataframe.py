import pandas as pd

def timestream_query_to_dataframe(client, QueryString, MaxRows=100):
    initial_response = client.query(
        QueryString=QueryString,
        MaxRows=MaxRows
    )

    NextToken = initial_response.get('NextToken', None)

    responses = [initial_response]

    while NextToken:
        timestream_response = client.query(
            QueryString=QueryString,
            MaxRows=MaxRows,
            NextToken=NextToken
        )
        responses.append(timestream_response)
        NextToken = timestream_response.get('NextToken', None)

    output_frame = (
        pd
        .DataFrame([
            {
                col['Name']: val['ScalarValue']
                for col, val in zip(response['ColumnInfo'], row['Data'])
            }
            for response in responses
            for row in response['Rows']
        ])
    )

    return output_frame