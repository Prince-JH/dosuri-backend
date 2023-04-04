from celery import shared_task
from dosuri.common import utils as cu
from dosuri.common import sms as cs
from dosuri.common import slack as csl
from django.conf import settings


@shared_task
def announce_insurance_consult(message):
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, settings.INSURANCE_PHONE_NUMBERS)
    slack_client = csl.SlackClient()
    slack_client.send_message_to_bot_channel(message)


@shared_task
def announce_insurance_consult_to_user(phone_no):
    phone_no = phone_no.replace('-', '')
    message = '[도수리] \n' \
              '실손보험 담당자가 곧 연락드릴 예정입니다. \n' \
              '곽혜경 010-9071-4800'
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, [phone_no])
