import boto3
import json
import base64
import hashlib
import cgi
from requests_toolbelt.multipart import decoder
import os

BUCKET_NAME = 'dosuri-image'
FILE_PATH = 'uploads/'

response  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

WAS_ENDPOINT = os.environ['WAS_SERVER']

s3 = boto3.client('s3')

def string_escape(s, encoding='utf-8'):
    return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('latin1')         # 1:1 mapping back to bytes
             .decode(encoding))        # Decode original encoding

def lambda_handler(event, context):
    content = ''
    headers = ''
    
    body = base64.b64decode(event['body-json']) 
    
    if 'content-type' in event['params']['header']:
        content_type = event['params']['header']['content-type']
    else:
        content_type = event['params']['header']['Content-Type']
    
    decode = decoder.MultipartDecoder(body,content_type)
    file_name = ""
    for part in decode.parts:
        content = part.content
        headers = part.headers
        value, params = cgi.parse_header(str(part.headers[b'Content-Disposition']))
        if params['name'] == 'file':
            file_name = string_escape(params['filename'])
            data = part.content
    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=FILE_PATH+file_name, Body=data)
    except Exception as e:
        raise IOError(e)
    response['body'] = {
        'bucket_name': BUCKET_NAME,
        'path': f'{FILE_PATH}{file_name}'
    }
    return response