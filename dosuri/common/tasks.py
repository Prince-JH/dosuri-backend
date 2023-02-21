from celery import shared_task
from dosuri.common import utils as cu


@shared_task
def announce_insurance_consult(message):
    cu.send_sms(message)
    cu.send_slack(message)
