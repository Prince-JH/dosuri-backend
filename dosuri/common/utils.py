import traceback
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
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


def rsa_signer(message):
    with open(settings.DOSURI_IMAGE_PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


cloudfront_signer = CloudFrontSigner(settings.DOSURI_IMAGE_PUBLIC_KEY_ID, rsa_signer)


def generate_signed_path(obj):
    try:
        url = f'http://{obj.bucket_name}.{settings.HOST_DOMAIN}/{parse.quote(obj.path)}'
        expire_date = timezone.now() + timedelta(days=1)

        signed_url = cloudfront_signer.generate_presigned_url(
            url, date_less_than=expire_date)
        return signed_url
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
