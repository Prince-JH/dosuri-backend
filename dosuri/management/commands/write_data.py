import json
import os

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from dosuri.user.models import User

import csv
import os.path
from datetime import datetime

from dosuri.common import utils as cu
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
