import boto3
from django.conf import settings

# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-northeast-1"
)


def send_sms(message):
    client.publish(
        Message=message,
        TopicArn='arn:aws:sns:ap-northeast-1:024317434110:dosuri-sms'
    )
