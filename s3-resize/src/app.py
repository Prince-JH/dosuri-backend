from io import BytesIO

import os
import requests
import json
import boto3

from urllib.parse import unquote_plus, quote_plus
from PIL import Image

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def resize_image(image, resize_bucket, key):
    in_mem_file = BytesIO()
    with Image.open(BytesIO(image)) as im:
        im.thumbnail((480, 480))
        im.save(in_mem_file, format=im.format)
        in_mem_file.seek(0)
        s3_client.put_object(
            Body=in_mem_file,
            Bucket=resize_bucket,
            Key=key
        )


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = s3.Bucket(os.environ.get('SOURCE_BUCKET_NAME'))
        resize_bucket = bucket + '-resized'
        key = unquote_plus(record['s3']['object']['key'])
        image = bucket.Object(key).get()['Body'].read()

        values = key.split('/')
        uuid = values[1]
        resize_image(image, resize_bucket, key)
        notify_job_finished(uuid, resize_bucket)


def notify_job_finished(uuid, resize_bucket):
    url = f"{os.environ.get('DOSURI_URL', 'https://server.dosuri.site')}/common/v1/attachment/{uuid}"
    data = {
        'bucket': resize_bucket
    }
    header = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    requests.patch(url, headers=header, data=json.dumps(data))
