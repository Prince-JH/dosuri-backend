import time

from django.core.management.base import BaseCommand
from dosuri.common.geocoding import KaKaoGeoClient
from dosuri.user import (
    models as um,
    constants as uc
)


class Command(BaseCommand):
    help = 'Set default address for users who do not have any.'

    def handle(self, *args, **options):
        set_default_address()


def set_default_address():
    client = KaKaoGeoClient()
    assocs = um.AddressUserAssoc.objects.all().select_related('address')
    for assoc in assocs:
        if um.UserAddress.objects.filter(user=assoc.user).exists():
            print(f'{assoc.user.username} address already exists.')
            continue
        print('address:', assoc.address.small_area)
        res = client.query_public_institutions_by_address(assoc.address.small_area)
        place = res['documents'][0]
        data = {
            'user': assoc.user,
            'name': assoc.address.small_area,
            'address': place['address_name'],
            'address_type': uc.ADDRESS_ETC,
            'latitude': place['y'],
            'longitude': place['x']
        }
        print('data', data)
        address = um.UserAddress.objects.create_address(data)
        um.UserAddress.objects.set_main_address(address)
        time.sleep(0.5)
    # print('locations:', list(locations))
