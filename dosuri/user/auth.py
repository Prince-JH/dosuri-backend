import json
import traceback
from datetime import datetime
import jwt
from django.utils import timezone
from django.utils.timezone import timedelta

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

APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"


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
        self.redirect_uri = self.get_redirect_uri()

    def get_user_info(self):
        access_token = self.get_access_token()
        kakao_user_info = self.get_kakao_user_info(access_token)
        user_info = self.pick_usable_info(kakao_user_info)
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

    def get_kakao_user_info(self, access_token):
        url = 'https://kapi.kakao.com/v2/user/me'
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        return self.get(url, self.set_api_header(**header))

    def get_redirect_uri(self):
        if settings.SERVER_URL in self.origin:
            return settings.KAKAO_REDIRECT_URI
        else:
            return 'http://localhost:3000/oauth/callback/kakao'

    def pick_usable_info(self, kakao_user_info):
        username = kakao_user_info['kakao_account'].get('email')
        name = kakao_user_info['kakao_account'].get('name')
        sex = kakao_user_info['kakao_account'].get('gender')
        if sex == 'male':
            sex = '남자'
        elif sex == 'female':
            sex = '여자'
        phone_no = kakao_user_info['kakao_account'].get('phone_number')
        if phone_no:
            country_code, phone_no = phone_no.split(' ')[0], phone_no.split(' ')[1]
            if country_code != '+82':
                phone_no = None
            phone_no = '0' + phone_no
        birth_year = kakao_user_info['kakao_account'].get('birthyear')
        birthday = kakao_user_info['kakao_account'].get('birthday')
        if birth_year and birthday:
            birthday = datetime.strptime(f'{birth_year}-{birthday}', '%Y-%m%d').astimezone()
        else:
            birthday = None
        return {'username': username, 'name': name, 'phone_no': phone_no, 'sex': sex, 'birthday': birthday}


class GoogleAuth(SocialAuth):
    def __init__(self, code, origin):
        self.code = code
        self.origin = origin
        self.redirect_uri = self.get_redirect_uri()

    def get_user_info(self):
        access_token = self.get_access_token()
        google_user_info = self.get_google_user_info(access_token)
        user_info = self.pick_usable_info(google_user_info)
        return user_info

    def get_access_token(self):
        try:
            url = 'https://oauth2.googleapis.com/token?'
            header = {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
            url += f'grant_type=authorization_code&' \
                   f'client_id={settings.GOOGLE_CLIENT_ID}&' \
                   f'client_secret={settings.GOOGLE_CLIENT_SECRET}&' \
                   f'redirect_uri={self.redirect_uri}&' \
                   f'code={self.code}'
            res = self.post(url, self.set_api_header(**header))
            return res['access_token']
        except APIException:
            raise uexc.GoogleApiException(json.loads(res.content))

    def get_google_user_info(self, access_token):
        url = 'https://openidconnect.googleapis.com/v1/userinfo'
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        return self.get(url, self.set_api_header(**header))

    def get_redirect_uri(self):
        if settings.SERVER_URL in self.origin:
            return settings.GOOGLE_REDIRECT_URI
        else:
            return 'http://localhost:3000/oauth/callback/kakao'

    def pick_usable_info(self, google_user_info):
        username = google_user_info.get('email')
        name = google_user_info.get('name')
        return {'username': username, 'name': name}


class AppleAuth(SocialAuth):
    def __init__(self, code, origin):
        self.code = code
        self.origin = origin

    def get_user_info(self):
        access_token = self.get_access_token()
        user_info = self.pick_usable_info(access_token)
        return user_info

    def get_access_token(self):
        return self.code

    def get_key_and_secret(self):
        headers = {
            'kid': settings.SOCIAL_AUTH_APPLE_KEY_ID
        }
        payload = {
            'iss': settings.SOCIAL_AUTH_APPLE_TEAM_ID,
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': settings.SOCIAL_AUTH_APPLE_CLIENT_ID,
        }

        client_secret = jwt.encode(
            payload,
            settings.SOCIAL_AUTH_APPLE_PRIVATE_KEY,
            algorithm='ES256',
            headers=headers
        )

        return settings.SOCIAL_AUTH_APPLE_CLIENT_ID, client_secret

    def pick_usable_info(self, apple_token):
        client_id, client_secret = self.get_key_and_secret()
        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': apple_token,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.SOCIAL_AUTH_APPLE_REDIRECT_URL
        }

        res = requests.post('https://appleid.apple.com/auth/token', data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)

        if id_token:
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            username = decoded['email'] if 'email' in decoded else None

        return {'username': username}
