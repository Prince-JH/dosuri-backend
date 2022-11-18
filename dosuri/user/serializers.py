from django.apps import apps

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    views as v,
    models as um,
    constants as c
)
from dosuri.common import models as cm
import requests


class Auth(s.Serializer):
    user_uuid: s.Field = s.CharField(read_only=True)
    token: s.Field = s.CharField(write_only=True)
    type: s.Field = s.CharField(write_only=True)
    access_token: s.Field = s.CharField(read_only=True)
    refresh_token: s.Field = s.CharField(read_only=True)
    is_new: s.Field = s.BooleanField(read_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        auth_domain = validated_data['type']
        if auth_domain == c.SOCIAL_KAKAO:
            auth_factory = a.KaKaoAuth(token)
        user_info = auth_factory.authenticate()
        username = user_info['email']

        user, is_new = um.User.objects.get_or_create_user(username)

        tokens = a.get_tokens_for_user(user)
        validated_data['access_token'] = tokens['access']
        validated_data['refresh_token'] = tokens['refresh']
        validated_data['is_new'] = is_new
        validated_data['user_uuid'] = user.uuid
        return validated_data


class User(s.Serializer):
    username: s.Field = s.CharField(read_only=True)
    nickname: s.Field = s.CharField(read_only=True)
    address_uuid: s.Field = s.SerializerMethodField('get_address_uuid')
    birthday: s.Field = s.DateTimeField(read_only=True)
    sex: s.Field = s.CharField(read_only=True)
    is_real: s.Field = s.BooleanField(read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    def get_address_uuid(self, obj):
        return cm.Address.objects.get_uuid_by_id(obj.address_id)
