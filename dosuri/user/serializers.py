from django.apps import apps

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    views as v,
    models as um,
    constants as c
)
import requests

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Auth(s.Serializer):
    user_uuid: s.Field = s.CharField(read_only=True)
    username: s.Field = s.CharField()
    token: s.Field = s.CharField(write_only=True)
    type: s.Field = s.CharField(write_only=True)
    access_token: s.Field = s.CharField(read_only=True)
    refresh_token: s.Field = s.CharField(read_only=True)
    is_new: s.Field = s.BooleanField(read_only=True)

    def create(self, validated_data):
        token = validated_data['token']
        username = validated_data['username']
        auth_domain = validated_data['type']
        auth_factory = a.SocialAuth(auth_domain)
        # if auth_domain == c.SOCIAL_KAKAKO:
        #     auth_factory.authenticate()
        # auth_factory = a.KaKaoAuth(kakao_token)
        # auth_factory.authenticate()

        user, is_new = um.User.objects.get_or_create_user(username)

        tokens = get_tokens_for_user(user)
        validated_data['access_token'] = tokens['access']
        validated_data['refresh_token'] = tokens['refresh']
        validated_data['is_new'] = is_new
        validated_data['user_uuid'] = user.uuid
        return validated_data


class User(s.ModelSerializer):
    nickname: s.Field = s.CharField(read_only=True)
    address_uuid: s.Field = s.CharField(read_only=True)
    birthday: s.Field = s.DateTimeField(read_only=True)
    sex: s.Field = s.CharField(read_only=True)
    is_real: s.Field = s.BooleanField(read_only=True)
    is_new: s.Field = s.BooleanField(read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = um.User
        exclude = ('id',)
