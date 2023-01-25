from django.core.management.base import BaseCommand
from dosuri.user.models import User

import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from dosuri.common import models as cm
from dosuri.hospital import (
    models as hm,
    constants as hc,
)


class Command(BaseCommand):
    help = 'Insert Hospital Data'

    def add_arguments(self, parser):
        parser.add_argument('data-type')
        parser.add_argument('file-loc')

    def handle(self, *args, **options):
        file_loc = options['file-loc']
        data_type = options['data-type']
        if data_type == 'hospital':
            read_hospital_data(file_loc)
        elif data_type == 'hospital_treatment':
            read_hospital_treatment_data(file_loc)
        elif data_type == 'hospital_image':
            read_hospital_image(file_loc)


def read_hospital_data(file_loc):
    loc = file_loc
    file = open(loc)
    reader = csv.reader(file)
    for line in reader:
        try:
            code = line[1]
            name = line[2]
            full_address = line[4]
            large_area = line[6]
            small_area = line[7]
            area = line[8]
            phone_no = line[9]
            opened_at = datetime.strptime(line[11], '%Y-%m-%d')
            longitude = line[19]
            latitude = line[20]
            status = line[21]
            status = hc.HOSPITAL_ACTIVE if status == '영업' else hc.HOSPITAL_INACTIVE

            print(code, name, full_address, large_area, small_area, area, phone_no, opened_at, longitude, latitude,
                  status)
            # if status == hc.HOSPITAL_ACTIVE:
            #     break
            # hospital_qs = hm.Hospital.objects.filter(code=code)
            # if hospital_qs.exists():
            #     hospital = hospital_qs.first()
            #     hospital.status = status
            #     hospital.save()
            # else:
            #     hospital_obj = hm.Hospital.objects.create(
            #         code=code,
            #         address=full_address,
            #         name=name,
            #         phone_no=phone_no,
            #         opened_at=opened_at,
            #         latitude=latitude,
            #         longitude=longitude,
            #         area=area,
            #         status=status
            #     )
            #     address_qs = cm.Address.objects.filter(large_area=large_area, small_area=small_area)
            #     if not address_qs.exists():
            #         address_obj = cm.Address.objects.create(
            #             large_area=large_area, small_area=small_area
            #         )
            #     hm.HospitalAddressAssoc.objects.create(
            #         hospital=hospital_obj,
            #         address=address_obj
            #     )
            #     print('INSERT:', code)
        except:
            pass


def read_hospital_treatment_data(file_loc):
    loc = file_loc
    file = open(loc)
    reader = csv.reader(file)

    for line in reader:
        code = line[0]
        name = line[4]
        price = line[5].replace(',', '')
        description = line[6]
        price_per_hour = line[7].replace(',', '') or None
        print(code, name, description, price, price_per_hour)

        try:
            hospital = hm.Hospital.objects.get(code=code)
            if not hm.HospitalTreatment.objects.filter(
                    hospital=hospital,
                    name=name,
                    price=price,
                    price_per_hour=price_per_hour,
                    description=description
            ).exists():
                hm.HospitalTreatment.objects.create(
                    hospital=hospital,
                    name=name,
                    price=price,
                    price_per_hour=price_per_hour,
                    description=description
                )
        except hm.Hospital.DoesNotExist:
            pass


def read_hospital_image(file_loc):
    import unicodedata
    import boto3
    from uuid import uuid4

    def generate_uuid():
        return uuid4().hex

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
