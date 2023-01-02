import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# Create an SNS client
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
