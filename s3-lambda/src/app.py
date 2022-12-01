from io import BytesIO

import os
import requests

import json
import boto3

from urllib.parse import unquote_plus, quote_plus
from PIL import Image

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def resize_image(image, key):
    in_mem_file = BytesIO()
    with Image.open(BytesIO(image)) as im:
        im.thumbnail((480, 480))
        im.save(in_mem_file, format=im.format)
        in_mem_file.seek(0)
        s3_client.put_object(
            Body=in_mem_file,
            Bucket=os.environ.get('SOURCE_BUCKET_NAME') + '-resized',
            Key=key
        )


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = s3.Bucket(os.environ.get('SOURCE_BUCKET_NAME'))
        key = unquote_plus(record['s3']['object']['key'])
        image = bucket.Object(key).get()['Body'].read()

        values = key.split('/')
        domain = values[0]
        uuid = values[1]
        path = 'https://dosuri-image.s3.ap-northeast-2.amazonaws.com/' + quote_plus(key)
        resize_image(image, key)
        notify_job_finished(domain, uuid, path)


def notify_job_finished(domain, uuid, path):
    url = f"{os.environ.get('DOSURI_URL', 'https://server.dosuri.site')}/hospital/v1/keywords/"
    data = {
        'name': path,
        'is_custom': True,
        'domain': domain
    }
    header = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    res = requests.post(url, headers=header, data=json.dumps(data))
