import json
import requests

from urllib import parse

from rest_framework import exceptions as exc
from django.conf import settings

from django.contrib.auth.backends import BaseBackend

from dosuri.user import models as um


class AuthenticationWithoutPassword(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = request.data.get('username', '')
        try:
            return um.User.objects.get(username=username)
        except um.User.DoesNotExist:
            return um.User.objects.create_user(username=username)

    def get_user(self, user_id):
        try:
            return um.User.objects.get(pk=user_id)
        except um.User.DoesNotExist:
            return None


class SocialAuth:
    def set_api_header(self, **kwargs):
        if not kwargs:
            return {
                'Content-Type': 'application/json; charset=utf-8',
            }
        else:
            return kwargs

    def get(self, url, headers, params=None):
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise exc.APIException()
        return response.json()

    def post(self, url, headers, data):
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code not in (200, 201):
            raise exc.APIException()
        return response.json()


class KaKaoAuth(SocialAuth):
    def __int__(self, token):
        self.token = token

    def authenticate(self):
        url = 'https://kauth.kakao.com/oauth/token'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'code': self.token,
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': parse.urlparse(f'{settings.SITE_URL}:3000/oauth/callback/kakao')
        }
        return self.post(url, self.set_api_header(header), data)

