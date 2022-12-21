try:
    import unzip_requirements
except ImportError:
    pass

try:
    import json
    import boto3
    import io
    import pandas as pd

except Exception as e:
    print("Error ***", e)

def hello(event, context):
    client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('s3trigger_serverless')

    for item in event.get("Records"):
        s3 = item.get("s3")
        bucket = s3.get("bucket").get("name")
        key = s3.get("object").get("key")

        print("bucket", bucket)
        print("key", key)

        # response_new = client.get_object(Bucket=bucket, Key=str(key))
        # df = pd.read_csv(io.BytesIO(response_new["Body"].read()))

        path = "s3://" + bucket+ "/" + key
        df = pd.read_csv(path, delimiter='\t')

        print(df.columns)
        
        with table.batch_writer() as batch:
            for index, row in df.iterrows():
                batch.put_item(json.loads(row.to_json()))


    response = {
        "statusCode": 200,
        "body": json.dumps("Process complete ")
    }