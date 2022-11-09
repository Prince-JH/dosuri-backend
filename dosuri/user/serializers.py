from django.apps import apps

from rest_framework import serializers as s
from dosuri.user import (
    auth as a
)


class KakaoAuth(s.Serializer):
    token: s.Field = s.CharField()

    def create(self, validated_data):
        token = validated_data['token']
        auth_factory = a.KaKaoAuth(token)
        auth_factory.authenticate()
        return validated_data
