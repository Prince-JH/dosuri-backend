import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image

import json
import boto3


s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def resize_image(image, resized_path):
    with Image.open(image) as image:
        image.resize((480, 480))
        image.save(resized_path)


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = s3.Bucket(os.environ.get('SOURCE_BUCKET_NAME'))
        key = unquote_plus(record['s3']['object']['key'])
        image = bucket.Object(key).get()
        upload_path = key
        resize_image(image, upload_path)
        s3_client.upload_file(upload_path, os.environ.get('SOURCE_BUCKET_NAME') + '-resized')
