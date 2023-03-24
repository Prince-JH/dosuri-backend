from io import BytesIO

import os
import requests
import json
import boto3

from urllib.parse import unquote_plus, quote_plus
from PIL import Image

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def resize_image(image, resize_bucket_name, key):
    in_mem_file = BytesIO(image)
    img = Image.open(in_mem_file)
    parsed_key = parse_key_wo_extension(key)
    img.convert('RGB')
    img.thumbnail((480, 480))
    img.save(in_mem_file, 'webp')
    in_mem_file.seek(0)
    resized_key = f'{parsed_key}.webp'

    s3_client.put_object(
        Body=in_mem_file,
        Bucket=resize_bucket_name,
        Key=resized_key
    )
    in_mem_file.close()
    return resized_key


def parse_key_wo_extension(key):
    return key.split('.')[0]


def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = os.environ.get('SOURCE_BUCKET_NAME')
        bucket = s3.Bucket(bucket_name)
        resize_bucket_name = bucket_name + '-resized'
        key = unquote_plus(record['s3']['object']['key'])
        image = bucket.Object(key).get()['Body'].read()

        values = key.split('/')
        uuid = values[0]
        key = resize_image(image, resize_bucket_name, key)
        notify_job_finished(uuid, resize_bucket_name, key)


def notify_job_finished(uuid, resize_bucket_name, key):
    url = f"{os.environ.get('DOSURI_URL', 'https://dev-server.dosuri.site')}/common/v1/attachment/{uuid}"
    data = {
        'bucket_name': resize_bucket_name,
        'path': f'{key}'
    }
    header = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    requests.patch(url, headers=header, data=json.dumps(data))
