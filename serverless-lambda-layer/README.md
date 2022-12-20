Deploying lambda function with external python packages using serverless framework. 

Overview:

Lambda Function & Layers: AWS Lambda is a computing service that allows us to run our code without the overhead of configuring and managing a server. It can be scaled automatically based on the request and the charge is calculated only for the compute time. Lambda function can be deployed using .zip file archive that contains function and the dependency or using container image. Lambda layers can be used to package external dependencies that is required to run lambda function. It promotes  sharing components that can be used in multiple lambda functions. It also helps in reducing the size of lambda function making it faster to deploy our code. 

We can manually create a lambda layer and add it to the lambda function. Lambda uses Amazon linux environment, so make sure your dependencies will work in that environment.  For each Lambda runtime, the PATH variable includes specific folders in the /opt directory. so, we should define the same folder structure in your layer .zip file archive. For python, python and python/lib/python{version}/site-packages are folder paths that runtime supports.

But serverless framework makes it easier as everything can be defined through the YAML file. Serverless Framework can be used to develop, deploy and troubleshoot serverless applications. 


Installing Serverless Framework:

Severless Framework requires node. So, if you don't have node on your machine, install it first. After that we can install serverless using: 

```
npm install -g serverless
```

Set up a user with minimal permissions that is required for your application and configure serverless framework by providing access and secret key from AWS.

```
serverless config credentials --provider aws --key '' --secret '' -o
```

Make sure you're using a virtual environment to isolate your python package installation.

```
python3 -m venv env
source env/bin/activate
```

Create a serverless function:

```
serverless create --template aws-python3 --name lambda-test --path lambda-test
```
or you can choose from the template provided by serverless framework using:

```
serverless
```

We can further install serverless-layers so that it attaches layers to the function and publishes a new layer whenever dependencies is updated.

```
npm install -D serverless-layers
```

Install plugin:

To deploy the content of requirements.txt, we need serverless-python-requirements plugin. This plugin bundles python dependencies specified in requirements.txt while running sls deploy. Plugins can be installed using:
```
sls plugin install --name pluginName
```
In this case pluginName will be replaced by serverless-python-requirements

```
sls plugin install --name serverless-python-requirements
```

Update the handler.py with the code that you want to run add the python pacakages that you need to run the code in requirements.txt

```
try:
    import unzip_requirements
except:
    pass
    
import json
import pandas as pd

def hello(event, context):

    data = {
        "name": ["Joe", "Steve"],
        "Department": ["Computer", "Mechanical"]
        }
    
    df= pd.DataFrame(data)
    print(df.head(2))
    return {"statusCode": 200, 
    "body": json.dumps('Demo lambda function to test pandas layer')}
```

Update the Serverless.yml file

```
service: serverless-demo-project

frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.8


plugins:
  - serverless-python-requirements

#serverless python requirements: https://www.serverless.com/plugins/serverless-python-requirements
#use the code upto usestaticCache if you want to use external libraries in requirements.txt ; the code in layer tag can be used to push AWS lambda layer
custom:
  pythonRequirements:
    dockerizePip: true
    zip: true
    useDownloadCache: false
    useStaticCache: false

    layer: 
      name: python-pandas
      description: "Layer which contains pandas library"
      compatibleRuntimes:
        - python3.8

functions:
  hello:
    handler: handler.hello
  

package:
  patterns:
    - '!**/*'
    - '*.py'
    - 'pandas'

```
Deploy serverless:

```
sls deploy
```

you can go the AWS lambda console to test the function or invoke function from console:

```
sls invoke -f 'functioname' --log
sls invoke -f hello --log
```

If you want to reuse the layer created after deploying this function, you can remove the custom code block and add layer arn to serverless.yml

```
provider:
  name: aws
  runtime: python3.8
  layers:
        - arn:aws:lambda:region:************:layer:python-pandas:1
        
```

To remove sls stack:
```
sls remove
```
