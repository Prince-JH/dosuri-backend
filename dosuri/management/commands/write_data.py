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

    def handle(self, *args, **options):
        data_type = options['data-type']
        if data_type == 'no_image_hospitals':
            write_no_image_hospitals()


def write_no_image_hospitals():
    codes = hm.Hospital.objects.filter(hospital_attachment_assoc__isnull=True).distinct().values_list('code', flat=True)
    file = '/Users/jihoon/Study/Django/dosuri-backend/no_image_hospitals.csv'

    with open(file, 'w') as f:
        writer = csv.writer(f)
        for code in codes:
            writer.writerow([code])
