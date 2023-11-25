import os

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
    s3 = boto3.client('s3')

    for root, dirs, files in os.walk(file_loc):
        print(f"Current directory: {root}")
        for file in files:
            hospital_uuid = root.split('/')[-1]
            hospital = hm.Hospital.objects.get(uuid=hospital_uuid)
            print(hospital)

            title = unicodedata.normalize('NFC', file.rstrip('.jpg'))
            qs = hm.Doctor.objects.filter(name=title, hospital=hospital)
            bucket = 'dosuri-image'
            if qs.exists():
                doctor = qs.first()
                if not hm.DoctorAttachmentAssoc.objects.filter(doctor=doctor).exists():
                    uuid = generate_uuid()
                    path = f'{uuid}/{title}'
                    s3.upload_file(f'{root}/{file}', bucket, path)
                    attachment = cm.Attachment.objects.create(
                        uuid=uuid,
                        bucket_name=bucket,
                        path=path
                    )
                    hm.DoctorAttachmentAssoc.objects.create(
                        doctor=doctor,
                        attachment=attachment
                    )
                    print(f'upload {path}')
