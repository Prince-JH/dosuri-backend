from celery import shared_task
from dosuri.common import utils as cu
from dosuri.common import sms as cs
from dosuri.common import slack as csl
from django.conf import settings
import datetime

import dosuri.community.models as cm


@shared_task
def announce_insurance_consult(message):
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, settings.INSURANCE_PHONE_NUMBERS)
    slack_client = csl.SlackClient()
    slack_client.send_message(message)


@shared_task
def announce_insurance_consult_to_user(phone_no):
    phone_no = phone_no.replace('-', '')
    message = '[도수리] \n' \
              '실손보험 담당자가 곧 연락드릴 예정입니다. \n' \
              '곽혜경 010-9071-4800'
    naver_client = cs.NaverCloudClient()
    naver_client.send_sms(message, [phone_no])

@shared_task
def article_relocation_every_day():
    today = datetime.date.today()
    article_list = cm.Article.objects.all().order_by('created_at')[:10]

    for article in article_list:
        article.created_at.year = today.year
        article.created_at.month = today.month
        article.created_at.day = today.day
        article.save()
    return


@shared_task
def test_batch_every_min():
    import datetime
    print("TEST_BATCH_RUNNING!")
    f = open('/home/ec2-user/batch.log', 'w')
 
    # 파일에 텍스트 쓰기
    f.write(datetime.datetime.now() + ':  Every min batch complete!')

    # 파일 닫기
    f.close()
    return
