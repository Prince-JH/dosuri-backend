from django.conf import settings

import hashlib
import hmac
import base64
import requests
import time
import json


class NaverCloudClient:
    def __init__(self, access_key=settings.NAVER_CLOUD_ACCESS_KEY_ID, secret_key=settings.NAVER_CLOUD_SECRET_KEY):
        self.access_key = access_key
        self.secret_key = secret_key

    def set_api_header(self, timestamp):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': self.make_signature(timestamp)
        }

    def make_signature(self, timestamp):
        access_key = self.access_key
        secret_key = bytes(self.secret_key, 'UTF-8')

        method = "POST"
        uri = "/sms/v2/services/ncp:sms:kr:303008356722:dosuri/messages"

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def send_sms(self, message, phone_numbers=settings.INSURANCE_PHONE_NUMBERS):
        if not isinstance(phone_numbers, list):
            phone_numbers = json.loads(phone_numbers)
        timestamp = str(int(time.time() * 1000))
        url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:303008356722:dosuri/messages'
        data = {
            "type": "SMS",
            "from": settings.NAVER_CLOUD_FROM_NUMBER,
            "content": message,
            "messages": [{'to': phone_number} for phone_number in phone_numbers]
        }
        res = requests.post(url=url, data=json.dumps(data), headers=self.set_api_header(timestamp))
        return res
