from celery import shared_task
from dosuri.common import utils as cu
from dosuri.common import sms as cs
from django.conf import settings


@shared_task
def announce_insurance_consult(message):
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, settings.INSURANCE_PHONE_NUMBERS)
    cu.send_slack(message)
