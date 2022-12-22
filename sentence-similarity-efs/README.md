# Mount AWS EFS volume into AWS Lambda with the Serverless Framework

One of the biggest challenge while deploying machine learning applications in AWS Lambda is the limited size of deployment package. It becomes more challenging when you are dealing with 'state of art' models like BERT. There are several ways to compress the models and use it in production. One of the technique is to mount EFS to the serverless function.

EFS is built to scale on demand to petabytes of data, growing and shrinking automatically as files are written and deleted. When used with Lambda, your code has low-latency access to a file system where data is persisted after the function terminates.

In this post, I am going to use sentence transformer to re-rank the sentences based on text similarity to a given query.

#### Creating an EFS file system and upload the required libraries and models 

The first step is to create an EFS file system. Then we can start an ec2 instance and mount the file system to install the required packages and models on EFS. The instance must have access to the same security group and reside in the same VPC as the EFS file system. 

#### Create a lambda function

Then, we can create a lambda function using serverless aws-python3 template.

we first need to initialize the model. paraphrase-MiniLM-L6-v2 is a sentence-transformers model which maps sentences & paragraphs to a 384 dimensional dense vector space and can be used for tasks like clustering or semantic search.

```
model = SentenceTransformer('/mnt/tmp/paraphrase-MiniLM-L6-v2')
```
 We can build sentence embeddings using the encode method.

```
embeddings= model.encode(documents)
query_embeddings= model.encode(query)
```

Once, we have the embeddings of both the sentences and query parameter, we can compare the sentence similarity using cosine similarity.

```
scores = cos_sim(query_embeddings, embeddings).flatten()
```

#### Configure serverless.yaml

Lambda functions that access EFS must also run within the same VPC. We need to provide the arn of the EFS access point and path under which the EFS is moounted in the lambda function.

```
fileSystemConfig:
      localMountPath: /mnt/tmp
      arn: arn:aws:elasticfilesystem:us-east-1:931955206531:access-point/fsap-08c6b99eba84f318e
    vpc:
      securityGroupIds:
        - sg-b774b4f9
      subnetIds:
        - subnet-40762e0a
        - subnet-42881d1e
        - subnet-97fc74f0
```


Since we are loading the required python libraries from the EFS, we need to provide python path to our lambda function.

```
environment:
   PYTHONPATH: "/mnt/tmp/lib"
```

#### Deploy and Test the function

To test the function, I am using AWS console and the snapshot of the result is attached below.

<figure>
  <img src="https://github.com/shikshya1/aws-serverless/blob/main/s3-trigger-event/images/dataframe.png?raw=true" />
</figure>

References:

https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/