from django.contrib.auth.models import AnonymousUser

from dosuri.common import geocoding as cg
from dosuri.user import models as um


class HospitalDistance:
    def get_coordinates(self):
        if isinstance(self.request.user, AnonymousUser):
            return self.get_default_coordinates()
        address = um.AddressUserAssoc.objects.get_user_address(self.request.user)
        if not address:
            return self.get_default_coordinates()
        client = cg.KaKaoGeoClient()
        return client.get_coordinates(address)

    def set_coordinates(self, latitude, longitude):
        is_realtime_coordinates = getattr(self, 'is_realtime_coordinates', False)
        if not is_realtime_coordinates:
            coordinates = self.get_coordinates()
            latitude = coordinates[0]
            longitude = coordinates[1]
        self.latitude = latitude
        self.longitude = longitude

    def get_queryset(self):
        try:
            latitude = float(self.request.GET.get('latitude'))
            longitude = float(self.request.GET.get('longitude'))
        except (ValueError, TypeError):
            return self.queryset
        self.set_coordinates(latitude, longitude)
        return self.queryset.annotate_distance(self.latitude, self.longitude)

    def get_default_coordinates(self):
        '''
        서울시 강남구의 좌표
        '''
        latitude = 37.517331925853
        longitude = 127.047377408384
        return [latitude, longitude]