import os
from django.core.management.base import BaseCommand
from dosuri.user.models import User

import csv
import os.path
from datetime import datetime

from dosuri.common import models as cm
from dosuri.hospital import models as hm


class Command(BaseCommand):
    help = 'Insert Hospital Data'

    def add_arguments(self, parser):
        parser.add_argument('file_loc')

    def handle(self, *args, **options):
        file_loc = options['file_loc']
        read_hospital_data(file_loc)


def read_hospital_data(file_loc):
    loc = file_loc
    file = open(loc)
    reader = csv.reader(file)
    for line in reader:
        code = line[0]
        name = line[1]
        full_address = line[4]
        longitude = line[20]
        latitude = line[21]
        addresses = full_address.split(' ')
        do, city, gun, gu = None, None, None, None
        for address in addresses:
            if address == '':
                continue
            elif address[-1] == '도':
                do = address
            elif address[-1] == '시':
                city = address
            elif address[-1] == '군':
                gun = address
            elif address[-1] == '구':
                gu = address
        phone_no = line[9]
        opened_at = datetime.strptime(line[11], '%Y-%m-%d')
        hospital_obj = hm.Hospital.objects.create(
            code=code,
            address=full_address,
            name=name,
            phone_no=phone_no,
            opened_at=opened_at,
            latitude=latitude,
            longitude=longitude
        )
        address_qs = cm.Address.objects.filter(do=do, city=city, gun=gun, gu=gu)
        if not address_qs.exists():
            address_obj = cm.Address.objects.create(
                do=do,
                city=city,
                gun=gu,
                gu=gu
            )
        hm.HospitalAddressAssoc.objects.create(
            hospital=hospital_obj,
            address=address_obj
        )
        print(do, city, gun, gu, phone_no, opened_at, latitude, longitude)
