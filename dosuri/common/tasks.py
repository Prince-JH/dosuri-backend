from celery import shared_task
from dosuri.common import utils as cu
from dosuri.common import sms as cs
from django.conf import settings


@shared_task
def announce_insurance_consult(message):
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, settings.INSURANCE_PHONE_NUMBERS)
    cu.send_slack(message)


@shared_task
def announce_insurance_consult_to_user(phone_no):
    message = '도수치료 리얼후기 도수리입니다. \n' \
              '실손보험 담당자가 곧 연락드릴 예정입니다. \n' \
              '곽혜경 010-9071-4800'
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, [phone_no])
