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

    def get_coordinates(self, address):
        result = self.query_address(address)
        latitude = float(result['documents'][0]['address']['y'])
        longitude = float(result['documents'][0]['address']['x'])
        return [latitude, longitude]
