import json
import traceback

import requests

from urllib import parse

from rest_framework import exceptions as exc
from django.conf import settings

from django.contrib.auth.backends import BaseBackend
from rest_framework.exceptions import APIException

from dosuri.user import (
    models as um,
    constants as c,
    exceptions as uexc
)
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
        response = requests.post(url, data=data, headers=headers)
        if response.status_code not in (200, 201):
            raise exc.APIException()
        return response.json()


class KaKaoAuth(SocialAuth):
    def __init__(self, code, origin):
        self.code = code
        self.origin = origin
        self.redirect_uri = self.get_redirect_uri(self.origin)

    def authenticate(self):
        access_token = self.get_access_token()
        user_info = self.get_user_info(access_token)
        return user_info

    def get_access_token(self):
        try:
            url = 'https://kauth.kakao.com/oauth/token'
            header = {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
            body = {
                'grant_type': 'authorization_code',
                'client_id': settings.KAKAO_REST_API_KEY,
                'redirect_uri': self.redirect_uri,
                'code': self.code
            }
            res = self.post(url, self.set_api_header(**header), body)
            return res['access_token']
        except APIException:
            raise uexc.KakaoApiException()

    def get_user_info(self, access_token):
        url = 'https://kapi.kakao.com/v2/user/me'
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        return self.get(url, self.set_api_header(**header))

    def get_redirect_uri(self, origin):
        if settings.SERVER_URL in origin:
            return settings.KAKAO_REDIRECT_URI
        else:
            return 'http://localhost:3000/oauth/callback/kakao'


class GoogleAuth(SocialAuth):
    def __init__(self, code, origin):
        self.code = code
        self.origin = origin
        self.redirect_uri = self.get_redirect_uri(self.origin)

    def authenticate(self):
        access_token = self.get_access_token()
        user_info = self.get_user_info(access_token)
        return user_info

    def get_access_token(self):
        try:
            url = 'https://oauth2.googleapis.com/token'
            header = {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
            body = {
                'grant_type': 'authorization_code',
                'client_id': settings.GOOGLE_CLEINT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': self.redirect_uri,
                'code': self.code
            }
            res = self.post(url, self.set_api_header(**header), body)
            return res['access_token']
        except APIException:
            raise uexc.GoogleApiException()

    def get_user_info(self, access_token):
        url = 'https://kapi.kakao.com/v2/user/me'
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        return self.get(url, self.set_api_header(**header))

    def get_redirect_uri(self, origin):
        if settings.SERVER_URL in origin:
            return settings.GOOGLE_REDIRECT_URI
