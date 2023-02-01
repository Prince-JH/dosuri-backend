from dosuri.common import geocoding as cg
from dosuri.user import models as um
from dosuri.hospital import exceptions as hexc


class HospitalDistance:
    def get_coordinates(self):
        address = um.AddressUserAssoc.objects.get_user_address(self.request.user)
        if not address:
            return
        client = cg.KaKaoGeoClient()
        return client.get_coordinates(address)

    def set_coordinates(self, latitude, longitude):
        if latitude == '0' and longitude == '0':
            coordinates = self.get_coordinates()
            if not coordinates:
                raise hexc.NoAddress()
            latitude = coordinates[0]
            longitude = coordinates[1]
        else:
            latitude = float(latitude)
            longitude = float(longitude)
        self.latitude = latitude
        self.longitude = longitude

    def get_queryset(self):
        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')

        if not latitude or not longitude:
            return self.queryset
        try:
            self.set_coordinates(latitude, longitude)
        except hexc.NoAddress:
            return self.queryset
        return self.queryset.annotate_distance(self.latitude, self.longitude)
