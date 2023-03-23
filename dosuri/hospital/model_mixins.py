import random

from django.contrib.auth.models import AnonymousUser

from dosuri.common import geocoding as cg
from dosuri.user import models as um


class HospitalDistance:
    def get_coordinates(self):
        client = cg.KaKaoGeoClient()
        if isinstance(self.request.user, AnonymousUser):
            return self.get_default_coordinates(client)
        address = um.AddressUserAssoc.objects.get_user_address(self.request.user)
        if not address:
            return self.get_default_coordinates(client)
        return client.get_coordinates('address', address)

    def set_coordinates(self):
        is_realtime_coordinates = getattr(self, 'is_realtime_coordinates', False)
        if is_realtime_coordinates:
            try:
                latitude = float(self.request.GET.get('latitude'))
                longitude = float(self.request.GET.get('longitude'))
            except (ValueError, TypeError):
                return
        else:
            coordinates = self.get_coordinates()
            latitude = coordinates[0]
            longitude = coordinates[1]
        setattr(self, 'latitude', latitude)
        setattr(self, 'longitude', longitude)
        return [latitude, longitude]

    def get_queryset(self):
        set_coordinates = self.set_coordinates()
        if not set_coordinates:
            return self.queryset
        return self.queryset.annotate_distance(self.latitude, self.longitude)

    def get_default_coordinates(self, client):
        station = random.choice(['강남역', '봉천역', '발산역', '노원역', '잠실역'])
        return client.get_coordinates('station', station)
