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

### Manage permission

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

```
events:
        - s3:
            bucket: serverless-s3trigger-demo
            event: s3:ObjectCreated:*
            rules:
              - prefix: media-files/
              - suffix: .csv
            existing: true
```


After running deploy, you should see output similar to:

```bash
Deploying aws-python-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-project-dev (112s)

functions:
  hello: aws-python-project-dev-hello (1.5 kB)
```

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
serverless invoke --function hello
```

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"Go Serverless v3.0! Your function executed successfully!\", \"input\": {}}"
}
```

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function hello
```

Which should result in response similar to the following:

```
{
    "statusCode": 200,
    "body": "{\"message\": \"Go Serverless v3.0! Your function executed successfully!\", \"input\": {}}"
}
```

### Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
