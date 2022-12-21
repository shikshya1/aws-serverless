# Create a trigger to upload data in csv files to DynamoDB when csv is inserted on S3 via Lambda function using Serverless Framework 

This template demonstrates how to process a csv file when inserted on s3 bucket and use the data to populate DynamoDB table.  DynamoDB is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale.I am only using DynamoDB in this project for test purpose as it is a bad choice when we are dealing with small size of data. 

## Steps

#### Initialize a aws-python template from serverless framework

We then need to import boto3 (Python SDK that allows us to interact with DynamoDB and S3), pandas and s3fs (to read the csv file) library. We need to create a reference to our s3 bucket and DynamoDB table using:

```
client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('<TABLE-NAME>')
```
The snapshot of the dataframe that I will be working with is displayed below.

<figure>
  <img src="https://github.com/shikshya1/aws-serverless/blob/main/s3-trigger-event/images/dataframe.png?raw=true" />
</figure>

BatchNumber and StudentId columns are used as partition key and sort in DynamoDB table respectively.

We will extract the information about the csv path through Amazon S3 Event Notifications and read the records. We will then use batch writer to write objects to Amazon DynamoDB in batch.

```
for item in event.get("Records"):
        s3 = item.get("s3")
        bucket = s3.get("bucket").get("name")
        key = s3.get("object").get("key")

        print("bucket", bucket)
        print("key", key)

        path = "s3://" + bucket+ "/" + key
        df = pd.read_csv(path, delimiter='\t')

        print(df.columns)

        with table.batch_writer() as batch:
            for index, row in df.iterrows():
                batch.put_item(json.loads(row.to_json()))
```

### serverless.yaml file walkthrough

#### Manage permission

We will need proper IAM Permissions in order to read file from s3 bucket and interact with DynamoDB. Inside the serverless.yml file make the following adjustments:

```
iamRoleStatements:
    - Effect: Allow
      Action:
        - s3:*
      Resource: 
       - 'arn:aws:s3:::<bucket-name>/*'
    - Effect: Allow
      Action:
        - dynamodb:*
      Resource:
        - arn:aws:dynamodb:us-east-1:931955206531:table/<table-name>
```
#### Layers

As we will need pandas and s3fs to read the csv files, I will be providing the ARN's of the lambda layers of both of these libraries that I created while working on different project. 

```
layers:
        - arn:aws:lambda:us-east-1:931955206531:layer:pandas-numpy:1
        - arn:aws:lambda:us-east-1:931955206531:layer:s3fs:3
```

#### Event definition

The hello function is called whenever a document with .csv extension is uploaded to folder media-files in the bucket. This will reference serverless-s3trigger-demo bucket.


```
functions:
  hello:
    handler: handler.hello
    events:
        - s3:
            bucket: serverless-s3trigger-demo
            event: s3:ObjectCreated:*
            rules:
              - prefix: media-files/
              - suffix: .csv
            existing: true
```

