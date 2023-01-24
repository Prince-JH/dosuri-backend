import traceback
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from urllib import parse

# Create an SNS client
from django.utils import timezone

def generate_signed_path(obj):
    try:
        url = f'http://{obj.bucket_name}.{settings.HOST_DOMAIN}/{parse.quote(obj.path)}'
        return url
    except:
        traceback.print_exc()
        return None


def send_sms(message):
    sns_client.publish(
        Message=message,
        TopicArn='arn:aws:sns:ap-northeast-1:024317434110:dosuri-sms'
    )


def generate_presigned_url(bucket_name, key):
    try:
        return s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name, 'Key': key},
                                                ExpiresIn=3600)
    except ClientError as e:
        return None
