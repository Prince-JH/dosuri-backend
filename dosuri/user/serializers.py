from django.apps import apps

from rest_framework import serializers as s
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dosuri.user import (
    auth as a
)


class KakaoAuth(s.Serializer):
    token: s.Field = s.CharField()

    def create(self, validated_data):
        token = validated_data['token']
        auth_factory = a.KaKaoAuth(token)
        # auth_factory.authenticate()

        token_factory = v.TokenObtainPairWithoutPasswordView()
        return token_factory.post(request=request,username=username)


class TokenObtainPairWithoutPassword(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['password'].read_only = True

    def validate(self, attrs):
        attrs.update({'password': ''})
        print(attrs)
        return super(TokenObtainPairWithoutPassword, self).validate(attrs)
