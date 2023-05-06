import requests
from django.conf import settings
from urllib import parse
from rest_framework import exceptions as exc


class KaKaoGeoClient:
    def __init__(self, token=settings.KAKAO_REST_API_KEY):
        self.token = token

    def set_api_header(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'KakaoAK {self.token}'
        }

    def query_address(self, address):
        parsed_address = parse.quote(address)
        url = f'https://dapi.kakao.com/v2/local/search/address.json?query={parsed_address}'
        response = requests.get(url, headers=self.set_api_header())
        if response.status_code != 200:
            raise exc.APIException()
        return response.json()

    def query_station(self, station):
        parsed_station = parse.quote(station)
        url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={parsed_station}&category_group_code=SW8'
        response = requests.get(url, headers=self.set_api_header())
        if response.status_code != 200:
            raise exc.APIException()
        return response.json()

    def query_public_institutions_by_address(self, address):
        parsed_address = parse.quote(address)
        url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={parsed_address}&category_group_code=PO3'
        response = requests.get(url, headers=self.set_api_header())
        if response.status_code != 200:
            raise exc.APIException()
        return response.json()

    def get_coordinates(self, query_type, query):
        if query_type == 'address':
            result = self.query_address(query)
            latitude = float(result['documents'][0]['address']['y'])
            longitude = float(result['documents'][0]['address']['x'])
        elif query_type == 'station':
            result = self.query_station(query)
            latitude = float(result['documents'][0]['y'])
            longitude = float(result['documents'][0]['x'])
        if result['meta']['total_count'] == 0:
            return

        return [latitude, longitude]
