import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import time

service = 'es'
region = 'us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

def detect_labels(photo, bucket):

     client = boto3.client('rekognition',region_name='us-east-1')

     response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
     MaxLabels=10,
     # Uncomment to use image properties and filtration settings
     #Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
     #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
     # "ImageProperties": {"MaxDominantColors":10}}
     )

     print('Detected labels for ' + photo)
     
     for label in response['Labels']:
         print("LABEL =",label)
         print("Label: " + label['Name'])
         print("Confidence: " + str(label['Confidence']))
         print("Instances:")

         for instance in label['Instances']:
             print(" Bounding box")
             print(" Top: " + str(instance['BoundingBox']['Top']))
             print(" Left: " + str(instance['BoundingBox']['Left']))
             print(" Width: " + str(instance['BoundingBox']['Width']))
             print(" Height: " + str(instance['BoundingBox']['Height']))
             print(" Confidence: " + str(instance['Confidence']))
             print()

         print("Parents:")
         for parent in label['Parents']:
            print(" " + parent['Name'])
         
        #  print("Aliases:")
        #  for alias in label['Aliases']:
        #      print(" " + alias['Name'])

        #      print("Categories:")
        #  for category in label['Categories']:
        #      print(" " + category['Name'])
        #      print("----------")
        #      print()

     if "ImageProperties" in str(response):
         print("Background:")
         print(response["ImageProperties"]["Background"])
         print()
         print("Foreground:")
         print(response["ImageProperties"]["Foreground"])
         print()
         print("Quality:")
         print(response["ImageProperties"]["Quality"])
         print()

     return response['Labels']

def lambda_handler(event, context):
    # # TODO implement
    # # print("AWSAUTH =",credentials.access_key)
    # print("EVENT =",event)
    # print("CONTEXT=",context)
    # # osclient = boto3.client('opensearchserverless')
    # # response = osclient.batch_get_collection(
    # #     names=['photos'])
    
    # # dom = osclient.describe_domain(DomainName='photos')
    # # print("BOTO CONNECTED")
    
    # # print(dom)
    
    # bucket = event["Records"][0]["s3"]["bucket"]["name"]
    # photo = event["Records"][0]["s3"]["object"]["key"]
    # timestamp = event["Records"][0]["eventTime"]
    # print("BUCKET =",bucket)
    # print("PHOTO =",photo)
    # print("TIMESTAMP =",timestamp)
    

    bucket = "cloud-photos-b2"
    photo = "NN_results.png"
    s3client = boto3.resource('s3')
    print("s3CLIENT = ",s3client)
    # s3object = s3client.list_buckets()
    obj = s3client.Object(bucket_name=bucket,key=photo)
    print("OBJNAME =",obj.bucket_name)
    print("OBJKEY =",obj.key)
    
    s3object = obj.get()
    print("S3OBJECT = ",s3object)
    
    # labels = detect_labels(photo,bucket)
    # print("LABELS =",labels)

    # client = OpenSearch(
    #     hosts=[{'host': "search-photos-zzfdjlvipmphkf3veh6wv4xxpi.us-east-1.es.amazonaws.com", 'port': 443}],
    #     http_auth=awsauth,
    #     use_ssl=True,
    #     verify_certs=True,
    #     connection_class=RequestsHttpConnection,
    #     timeout=100000
    # )
    # print("client =",client)
    # # # It can take up to a minute for data access rules to be enforced
    # # # time.sleep(45)
    # # print("SLEEPING!!!!!")

    
    # index = 'photos'
    # # # response = client.search(index=index, body=query)
    # if not client.indices.exists('photos'):
    #     response = client.indices.create('photos')
    #     print('Checking index created:')
    #     print(response)
    # # else:
    # #     response = client.indices.get('photos')
    # #     print("Getting index:")
    # #     print(response)
    
    # jsonobj = {
    #     "objectKey":photo,
    #     "bucket":bucket,
    #     "createdTimestamp": timestamp,
    #     "labels":[ label["Name"] for label in labels]
    # }
    # print("Uploading object:")
    # print(jsonobj)
    # response = client.index(index='photos',body=jsonobj)
    # print('Indexed:')
    # print(response)

    # print("number of objects in index:")
    # client.indices.refresh(index="photos")
    # print(client.cat.count(index='photos'))

    # # query = {
    # #     "query": {
    # #     "must":{
    # #     "match":{
    # #     ""
    # #     }
    # #     }
    # #     }
    # # }
    # # response = client.index.search()
    # # response = client.search(index= 'photos', q='labels:Daisy')
    # # print("QUERY RESPONSE =",response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# lambda_handler(0,0)