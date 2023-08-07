from django.core.management.base import BaseCommand

from os import listdir
from os.path import isfile, join
from dosuri.common import models as cm
from dosuri.hospital import (
    models as hm,
    constants as hc,
)
import unicodedata
import boto3
from uuid import uuid4


class Command(BaseCommand):
    help = 'Upload Image'

    def add_arguments(self, parser):
        parser.add_argument('dir')

    def handle(self, *args, **options):
        dir = options['dir']
        upload_image(dir)


def generate_uuid():
    return uuid4().hex


def upload_image(file_loc):
    loc = file_loc
    files = [f for f in listdir(loc) if isfile(join(loc, f))]

    count = 1

    s3 = boto3.client('s3')
    for file in files:
        title = unicodedata.normalize('NFC', file.rstrip('.jpg'))
        code = title[:-2]
        qs = hm.Hospital.objects.filter(code=code)
        bucket = 'dosuri-image'
        if qs.exists():
            hospital = qs.first()
            uuid = generate_uuid()
            path = f'{uuid}/{title}'
            s3.upload_file(f'{file_loc}/{file.title()}', bucket, path)
            attachment = cm.Attachment.objects.create(
                uuid=uuid,
                bucket_name=bucket,
                path=path
            )
            assoc = hm.HospitalAttachmentAssoc.objects.create(
                hospital=hospital,
                attachment=attachment
            )
            print(count)
            count += 1
