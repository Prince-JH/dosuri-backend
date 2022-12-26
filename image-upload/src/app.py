import boto3
import json
import base64
import hashlib
from requests_toolbelt.multipart import decoder

BUCKET_NAME = 'dosuri-image'

response = {
    'statusCode': 200,
    'body': ''
}


def lambda_handler(event, context):
    # s3 = boto3.client('s3')
    print('body:', event['body'])
    print('headers:', event['headers'])
    # res['headers'] = event['headers']
    # res['body'] = event['body']
    decode = decoder.MultipartDecoder(event['body'], event['headers']['content-type'])
    #
    #
    for part in decode.parts:
        print('part.content:', part.content)
        print('part.headers:', part.headers)
        headers = part.headers
    #     res['content'].append(content)
    #     res['headers'].append(headers)

    # try:
    #     s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=full_name, Body=content)
    # except Exception as e:
    #     raise IOError(e)
    # response['body'] = json.dumps({'url': f'{"s3 image url 경로"}/{file_path}{file_name}.jpg'})
    return response
