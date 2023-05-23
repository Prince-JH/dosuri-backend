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
)
from dosuri.hospital import (
    models as hm,
    constants as hc,
)


class Command(BaseCommand):
    help = 'Get hospital ranks by treatment price'

    def handle(self, *args, **options):
        set_partner_hospitals()


def set_partner_hospitals():
    client = KaKaoGeoClient()
    stations = ['강남역', '봉천역', '발산역', '노원역', '잠실역']
    for station in stations:
        coordinates = client.get_coordinates('station', station)
        latitude = coordinates[0]
        longitude = coordinates[1]
        distance = 2
        latitude_range = get_latitude_range(latitude, distance)
        longitude_range = get_longitude_range(longitude, distance)
        hospitals = Hospital.objects.filter(latitude__range=latitude_range,
                                            longitude__range=longitude_range)
        hospitals.update(is_partner=True)


def get_latitude_range(latitude, km_distance):
    delta = round(km_distance / 111.19, 13)
    return round(latitude - delta, 13), round(latitude + delta, 13)


def get_longitude_range(longitude, km_distance):
    delta = round(km_distance / 88.80, 13)
    return round(longitude - delta, 13), round(longitude + delta, 13)
