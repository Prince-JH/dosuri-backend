import json
import os

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from dosuri.user.models import User

import csv
import os.path
from datetime import datetime

from dosuri.common import (
    utils as cu,
    models as cm,
)
from dosuri.hospital import (
    models as hm,
    constants as hc,
)


class Command(BaseCommand):
    help = 'Insert Hospital Data'

    def add_arguments(self, parser):
        parser.add_argument('data-type')

    def handle(self, *args, **options):
        data_type = options['data-type']
        if data_type == 'random_nickname':
            write_random_nickname()
        elif data_type == 'delete_images':
            delete_images()


def write_random_nickname():
    file = f'{settings.BASE_DIR}/dosuri/user/random_nickname.csv'
    nicknames = get_random_nickname()
    seed = 1
    requests.get(f'https://nickname.hwanmoo.kr/?format=json&count=3000&max_length=12&seed={seed}')
    seed += 1

    with open(file, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(nicknames)

    cu.s3_client.upload_file(file, 'dosuri-content', 'random_nickname.csv')


def get_random_nickname():
    nicknames = []

    seed = 1
    while len(nicknames) < 10000:
        content = json.loads(
            requests.get(f'https://nickname.hwanmoo.kr/?format=json&count=3000&max_length=8&seed={seed}').content)
        for word in content['words']:
            nicknames.append(word)
        seed += 1

    return nicknames


def delete_images():
    codes = [
        '강원도 철원군 서면 와수1로 16_한마음의원',
        '경기도 고양시 일산동구 중앙로 1059_일산이십일세기병원',
        '경기도 군포시 군포로 493_군포정형외과의원',
        '경기도 안산시 상록구 본오로 118_안산재활의학과의원',
        '경기도 안양시 동안구 동안로 128_범계정형외과의원',
        '경기도 안양시 동안구 시민대로 214_범계연세정형외과의원',
        '경기도 안양시 만안구 안양로 355_안양정형외과의원',
        '경기도 의정부시 평화로 636_바로정형외과의원',
        '경기도 화성시 동탄순환대로20길 118_서울바른정형외과의원',
        '대구광역시 달성군 화원읍 비슬로 2610_화원정형외과의원',
        '대구광역시 북구 칠곡중앙대로 302_태전정형외과연합의원',
        '대구광역시 수성구 동대구로 86_에스신경외과의원',
        '대전광역시 서구 계룡로 605_서울마취통증의학과의원',
        '부산광역시 금정구 금정로 244_금정병원',
        '서울특별시 강남구 봉은사로38길 12_더건강의원',
        '서울특별시 강서구 방화동로 40_서울정형외과의원',
        '서울특별시 관악구 신림로 198_바른의원',
        '서울특별시 구로구 가마산로 211_구로정형외과의원',
        '서울특별시 노원구 동일로 1393_노원신경정신과의원',
        '서울특별시 노원구 동일로 987_태릉마이크로병원',
        '서울특별시 동대문구 고산자로 476_서울정형외과의원',
        '서울특별시 동대문구 답십리로 64_성모정형외과의원',
        '서울특별시 서대문구 충정로 70_서대문정형외과의원',
        '인천광역시 미추홀구 경원대로897번길 1_인천정형외과의원'
    ]
    qs = hm.HospitalAttachmentAssoc.objects.exclude(hospital__uuid='934b7270d1964f478c41643ae0909ee6')
    print(qs.count())
    keys = list(qs.values_list('attachment__path', flat=True))
    # # keys = qs.values_list('path', flat=True)
    for key in keys:
        print(key)
        cu.s3_client.delete_object(Bucket='dosuri-image', Key=key)
    attachment_ids = list(qs.values_list('attachment', flat=True))
    cm.Attachment.objects.filter(id__in=attachment_ids).delete()
    qs.delete()
