import os
from django.core.management.base import BaseCommand
from dosuri.user.models import User

import csv
import os.path
from datetime import datetime

from dosuri.common import models as cm
from dosuri.hospital import models as hm


class Command(BaseCommand):
    def handle(self, *args, **options):
        read_hospital_data()


def read_hospital_data():
    url = os.path.join('/', 'Users', 'jihoon', 'Study', 'Django', 'hospital_data.csv')
    file = open(url)
    reader = csv.reader(file)
    for line in reader:
        code = line[0]
        name = line[1]
        full_address = line[4]
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
        dong = line[8] if line[8][-1] == '동' else None
        phone_no = line[9]
        opened_at = datetime.strptime(line[11], '%Y-%m-%d')
        print(do, city, gun, gu, dong, phone_no, opened_at)
        hospital_obj = hm.Hospital.objects.create(
            code=code,
            address=full_address,
            name=name,
            phone_no=phone_no,
            opened_at=opened_at
        )
        address_qs = cm.Address.objects.filter(do=do, city=city, gun=gun, gu=gu, dong=dong)
        if not address_qs.exists():
            address_obj = cm.Address.objects.create(
                do=do,
                city=city,
                gun=gu,
                gu=gu,
                dong=dong
            )
        hm.HospitalAddressAssoc.objects.create(
            hospital=hospital_obj,
            address=address_obj
        )
        break
