import json
import traceback
from datetime import datetime, timedelta

import boto3
import requests
from botocore.exceptions import ClientError
from django.conf import settings
from urllib import parse

# Create an SNS client
from django.utils import timezone

sns_client = boto3.client(
    "sns",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-northeast-1"
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-northeast-2"
)


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
        TopicArn=settings.AWS_SNS_TOPIC_ARN
    )


def send_slack(message):
    url = 'https://hooks.slack.com/services/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'
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {'text': message}
    return requests.post(url=url, data=json.dumps(data), headers=headers)


def generate_presigned_url(bucket_name, key):
    try:
        return s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name, 'Key': key},
                                                ExpiresIn=3600)
    except ClientError as e:
        return None
