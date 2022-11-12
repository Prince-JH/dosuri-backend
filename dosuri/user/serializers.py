from django.apps import apps

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    views as v,
    models as um
)
import requests

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class KakaoAuth(s.Serializer):
    username: s.Field = s.CharField(write_only=True)
    token: s.Field = s.CharField(write_only=True)
    access_token: s.Field = s.CharField(read_only=True)
    refresh_token: s.Field = s.CharField(read_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        username = validated_data['username']
        # auth_factory = a.KaKaoAuth(token)
        # auth_factory.authenticate()

        try:
            user = um.User.objects.get(username=username)
        except um.User.DoesNotExist:
            user = um.User.objects.create_user(username=username)
        tokens = get_tokens_for_user(user)
        validated_data['access_token'] = tokens['access']
        validated_data['refresh_token'] = tokens['refresh']
        return validated_data
