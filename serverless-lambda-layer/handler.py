try:
    import unzip_requirements
except:
    pass
    
import json
import pandas as pd

def hello(event, context):
    
    df= pd.DataFrame(data={'name':['shikshya']})
    print(df.shape)
    return {"statusCode": 200, 
    "body": json.dumps('hello')}
