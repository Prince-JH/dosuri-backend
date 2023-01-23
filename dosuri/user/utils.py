import csv
import os.path
from pathlib import Path
from random import randint

from django.db import transaction
from django.utils.module_loading import import_string
from storages.backends.s3boto3 import S3Boto3Storage

from dosuri.common import utils as cu
from django.conf import settings
from dosuri.user import models as um


def pick_random_nickname():
    storage_class = import_string(settings.CONTENT_STORAGE['class'])
    storage = storage_class(**settings.CONTENT_STORAGE.get('kwargs', {}))
    file = storage.open('random_nickname.csv')
    # csv_obj = cu.s3_client.get_object(Bucket='dosuri-content', Key='random_nickname.csv')
    # body = csv_obj['Body']
    # csv_string = body.read().decode('utf-8')
    reader = csv.reader(file.read().decode('utf-8').split('\r\n'))
    nicknames = next(reader)
    # for line in reader:
    #     print(line)
    #     break
    # nicknames = next(reader)
    random_number = randint(0, len(nicknames) - 1)
    return nicknames[random_number]


def get_random_nickname(candidate=None):
    with transaction.atomic():
        candidate = candidate or pick_random_nickname()
        qs = um.User.objects.filter(nickname=candidate)
        if not qs.exists():
            return candidate
        else:
            return candidate + str(qs.count())
