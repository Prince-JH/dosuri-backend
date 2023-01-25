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
    reader = csv.reader(file.read().decode('utf-8').split('\r\n'))
    nicknames = next(reader)
    random_number = randint(0, len(nicknames) - 1)
    return nicknames[random_number]


def get_random_nickname(candidate=None):
    with transaction.atomic():
        candidate = candidate or pick_random_nickname()
        while True:
            qs = um.User.objects.filter(nickname__startswith=candidate)
            if not qs.exists():
                return candidate
            elif qs.count() >= 100:
                candidate = pick_random_nickname()
            else:
                return candidate + str(qs.count())
