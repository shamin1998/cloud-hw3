import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

service = 'es'
region = 'us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)


def lambda_handler(event, context):
    print("EVENT =",event)
    print("CONTEXT =",context)
    
    # print("DETECTED INTENT =",event["interpretations"][0]["intent"]["name"])
    
    # if event["interpretations"][0]["intent"]["name"] != "SearchIntent":
        
    #     return {
    #         "sessionState" : {
    #             "dialogAction" : {
    #                 "type": "ElicitIntent",
    #                 "message":{
    #                     "contentType":"PlainText",
    #                     "content":"Would you like to search for a photo?"
    #                 }
    #             }
    #         }
    #     }
    
    # if "proposedNextState" in event.keys():
    #     if event["proposedNextState"]["dialogAction"]["type"] == "ElicitSlot":
    #         return {
    #             "sessionState" : event["proposedNextState"]
    #             }
    
    # label1 = "None"
    # label2 = "None"
    
    # if event["interpretations"][0]["intent"]["slots"]["label1"] != None:
    #     label1 = event["interpretations"][0]["intent"]["slots"]["label1"]["value"]["interpretedValue"]
    
    # if event["interpretations"][0]["intent"]["slots"]["label2"] != None:
    #     label2 = event["interpretations"][0]["intent"]["slots"]["label2"]["value"]["interpretedValue"]
    
    label1 = event["queryStringParameters"]["q"]
    print("LABEL1 = ",label1)
    # print("LABEL1 =",label1,", LABEL2 =",label2)

    client = OpenSearch(
        hosts=[{'host': "search-photos-zzfdjlvipmphkf3veh6wv4xxpi.us-east-1.es.amazonaws.com", 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=100000
    )
    print("client =",client)

    index = 'photos'
    response = client.search(index= index, q='labels:'+label1)
    print("QUERY RESPONSE =",response)

    bucket = "None"
    photo = "None"
    labels = []
    for hit in response["hits"]["hits"]:
        bucket = hit["_source"]["bucket"]
        photo = hit["_source"]["objectKey"]
        labels = hit["_source"]["labels"]
        break
    
    print("BUCKET =",bucket)
    print("PHOTO =",photo)

    s3client = boto3.resource('s3')
    print("s3CLIENT = ",s3client)
    # s3object = s3client.list_buckets()
    obj = s3client.Object(bucket_name=bucket,key=photo)
    print("OBJNAME =",obj.bucket_name)
    print("OBJKEY =",obj.key)
    
    # try:
    #     s3object = obj.get()
    #     print("S3OBJECT = ",s3object)
    # except:
    #     pass

    # response = {
    #     "sessionState": {
    #     #     "dialogAction" : {
    #     #             "type": "ElicitIntent",
    #     #             "message":{
    #     #                 "contentType":"PlainText",
    #     #                 "content":"Would you like to search for a photo?"
    #     #             }
    #     #         },
    #         'dialogAction': {
    #             "type":"Close",
    #             "fulfillmentState": "Fulfilled",
    #             "message": {
    #               "contentType": "PlainText",
    #               "content": "LF2 fulfilled"
    #             }
    #         },
    #         'intent' : event["interpretations"][0]["intent"]
    #     }
    # }
    
    # response["sessionState"]["intent"]["confirmationState"] = "Confirmed"
    # response["sessionState"]["intent"]["state"] = "Fulfilled"

    imageURL = "https://"+bucket+".s3.amazonaws.com/"+photo
    print("IMAGEURL = ",imageURL)
    # response["messages"] = [
    #     {
    #         "contentType":"ImageResponseCard",
    #         # "content" : "IntentResponse extra messages content",
    #         "imageResponseCard": {
    #             "title": photo,
    #             "subtitle": label1,
    #             "imageUrl": imageURL
    #             "buttons": [
    #                 {
    #                     "text": "stringtext",
    #                     "value": "stringvalue"
    #                 }
    #             ]
    #         }
    #     }]
    
    # print("SENDING RESPONSE =",response)
    photo = {
        "url" : imageURL,
        "labels" : labels
    }
    results = [photo]
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
        },
        'body': json.dumps({'results': results})
    }

    return response