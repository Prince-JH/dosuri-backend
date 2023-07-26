from django.core.management.base import BaseCommand

from dosuri.common.geocoding import KaKaoGeoClient
from dosuri.hospital.filters import HospitalDistanceFilter
from dosuri.hospital.models import Hospital
from dosuri.user.models import User

import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from dosuri.common import models as cm
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
    geocoding as cg,
)
from dosuri.hospital import (
    models as hm,
    constants as hc,
)


class Command(BaseCommand):
    help = 'Get hospital ranks by treatment price'

    def handle(self, *args, **options):
        get_hospital_rank_by_treatment_price()


def get_hospital_rank_by_treatment_price():
    file = 'hospital_ranks_in_points.txt'

    with open(file, 'w') as f:
        client = KaKaoGeoClient()
        stations = ['강남역', '봉천역', '발산역', '노원역', '잠실역']
        for station in stations:
            f.write(station)
            f.write('\n')
            f.write('\n')
            coordinates = client.get_coordinates('station', station)
            latitude = coordinates[0]
            longitude = coordinates[1]
            distance = 2
            latitude_range = cg.get_latitude_range(latitude, distance)
            longitude_range = cg.get_longitude_range(longitude, distance)
            hospitals = Hospital.objects.filter(latitude__range=latitude_range,
                                                longitude__range=longitude_range)
            f.write(f'총 병원 개수: {hospitals.count()}')
            f.write('\n')
            f.write('\n')

            hospitals_with_price = hospitals.get_queryset_with_avg_price_per_hour().order_by('avg_price_per_hour')
            f.write(f'가격이 있는 병원 개수: {hospitals_with_price.count()}')
            f.write('\n')
            f.write('\n')

            price = 0
            for hospital in hospitals_with_price:
                f.write(f'{hospital.name}, {hospital.avg_price_per_hour / 2}')
                f.write('\n')
                price += hospital.avg_price_per_hour / 2
            f.write('\n')
            f.write(f'30분당 가격의 평균값: {price / hospitals_with_price.count()}')
            f.write('\n')
            f.write('\n')
