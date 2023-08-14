import random
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from urllib.parse import unquote, quote
from dosuri.common import geocoding as cg
from dosuri.user import models as um
from dosuri.hospital import models as hm
from django.db.models import Avg


class HospitalCoordinates:
    def get_queryset(self):
        set_coordinates = self.set_coordinates()
        if not set_coordinates:
            return self.queryset
        return self.queryset.annotate_distance(self.latitude, self.longitude)

    def get_coordinates(self):
        client = cg.KaKaoGeoClient()
        if isinstance(self.request.user, AnonymousUser):
            return self.get_default_coordinates(client)
        address = um.UserAddress.objects.get_main_address(self.request.user)
        if not address:
            return self.get_default_coordinates(client)
        self.set_display_address(address.name)
        return [address.latitude, address.longitude]

    def set_coordinates(self):
        try:
            latitude = float(self.request.GET.get('latitude'))
            longitude = float(self.request.GET.get('longitude'))
        except (ValueError, TypeError):
            coordinates = self.get_coordinates()
            latitude = coordinates[0]
            longitude = coordinates[1]
        setattr(self, 'latitude', latitude)
        setattr(self, 'longitude', longitude)
        return [latitude, longitude]

    def set_display_address(self, display_address):
        setattr(self, 'address', display_address)

    def get_default_coordinates(self, client):
        if 'testserver' in self.request.build_absolute_uri():
            latitude = 37.517331925853
            longitude = 127.047377408384
            self.set_display_address('강남구')
            return [latitude, longitude]

        location = random.choice(['강남역', '봉천역', '발산역', '노원역', '잠실역'])
        self.set_display_address(location)
        return client.get_coordinates('station', location)

    def get_location_cookie(self, location_cookie):
        return unquote(location_cookie)

    def set_location_cookie(self, response):
        if isinstance(self.request.user, AnonymousUser) and not self.request.COOKIES.get('location'):
            response.set_cookie('location', quote(self.address), samesite='None', secure=True)


class HospitalSyncCoordinates(HospitalCoordinates):
    def get_default_coordinates(self, client):
        if 'testserver' in self.request.build_absolute_uri():
            latitude = 37.517331925853
            longitude = 127.047377408384
            self.set_display_address('강남구')
            return [latitude, longitude]

        location_cookie = self.request.COOKIES.get('location')
        if location_cookie:
            location = self.get_location_cookie(location_cookie)
        else:
            location = random.choice(['강남역', '봉천역', '발산역', '노원역', '잠실역'])
        self.set_display_address(location)
        return client.get_coordinates('station', location)


class HospitalPrice:
    def get_avg_price_per_hour(self, results):
        prices = []
        for result in results:
            price = result['price_per_hour']
            if price:
                prices.append(price)
        return sum(prices) / len(prices) if len(prices) > 0 else None


class HospitalRank:
    def get_hospital_rank(self, hospital_with_avg_price_per_hour, target_uuid):
        rank = 0
        last_avg_price_per_hour = None
        for count, hospital in enumerate(hospital_with_avg_price_per_hour):
            if last_avg_price_per_hour != hospital.avg_price_per_hour:
                rank = count + 1
            if hospital.uuid == target_uuid:
                return rank
            last_avg_price_per_hour = hospital.avg_price_per_hour

    def get_data_with_rank(self, request, client):
        target_uuid = request.GET.get('hospital')
        if not target_uuid:
            return None
        try:
            hospital = hm.Hospital.objects.get(uuid=target_uuid)
            if not hospital.is_partner:
                return None
            station = hospital.near_site
            coordinates = client.get_coordinates('station', station)
            latitude = coordinates[0]
            longitude = coordinates[1]
            distance_range = 2
            latitude_range = cg.get_latitude_range(latitude, distance_range)
            longitude_range = cg.get_longitude_range(longitude, distance_range)
            hospital_with_avg_price_per_hour = hm.Hospital.objects.filter(latitude__range=latitude_range,
                                                                          longitude__range=longitude_range) \
                .annotate_avg_price_per_hour().filter_has_avg_price_per_hour().order_by('avg_price_per_hour')
            rank = self.get_hospital_rank(hospital_with_avg_price_per_hour, target_uuid)

            return {'near_site': station, 'near_site_latitude': latitude, 'near_site_longitude': longitude,
                    'rank': rank, 'total_count': hospital_with_avg_price_per_hour.count(),
                    'avg_price_per_hour':
                        hospital_with_avg_price_per_hour.aggregate(total_avg_price_per_hour=Avg('avg_price_per_hour'))[
                            'total_avg_price_per_hour']}
        except hm.Hospital.objects.model.DoesNotExist:
            return None
