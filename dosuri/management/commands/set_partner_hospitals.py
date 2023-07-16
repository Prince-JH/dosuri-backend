from dosuri.common.geocoding import KaKaoGeoClient
from dosuri.hospital.models import Hospital
from django.core.management.base import BaseCommand

from dosuri.common import (
    geocoding as cg,
)


class Command(BaseCommand):
    help = 'Get hospital ranks by treatment price'

    def handle(self, *args, **options):
        set_partner_hospitals()


def set_partner_hospitals():
    client = KaKaoGeoClient()
    stations = ['강남역', '봉천역', '발산역', '노원역', '잠실역']
    Hospital.objects.all().update(near_site=None, is_partner=False)
    for station in stations:
        coordinates = client.get_coordinates('station', station)
        latitude = coordinates[0]
        longitude = coordinates[1]
        distance = 2
        latitude_range = cg.get_latitude_range(latitude, distance)
        longitude_range = cg.get_longitude_range(longitude, distance)
        hospitals = Hospital.objects.filter(latitude__range=latitude_range,
                                            longitude__range=longitude_range).filter_with_avg_price_per_hour()
        hospitals.update(near_site=station, is_partner=True)
    Hospital.objects.filter(name='강남밸런스의원').update(near_site='범계역', is_partner=True)
