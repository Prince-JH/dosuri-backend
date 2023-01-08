import datetime

from django.apps import apps
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    views as v,
    models as um,
    constants as c,
    serializer_schemas as sch,
    exceptions as exc
)
from dosuri.common import (
    models as cm,
    serializers as cs,
    utils as cu,
)


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

        origin = self.context['request'].build_absolute_uri()
        if 'server.dosuri.site' in origin:
            redirect_uri = 'https://dosuri.site/oauth/callback/kakao'
        else:
            redirect_uri = 'http://localhost:3000/oauth/callback/kakao'

        if auth_domain == c.SOCIAL_KAKAO:
            auth_factory = a.KaKaoAuth(token, redirect_uri)
        kakao_user_info = auth_factory.authenticate()
        username = kakao_user_info['kakao_account']['email']

        user = um.User.objects.get_or_create(username=username)[0]
        is_new = user.is_new()
        user_info = self.get_user_info_from_kakao(kakao_user_info)
        um.User.objects.update_user_info(user, user_info)
        tokens = a.get_tokens_for_user(user)

        validated_data['access_token'] = tokens['access']
        validated_data['refresh_token'] = tokens['refresh']
        validated_data['is_new'] = is_new
        validated_data['user_uuid'] = user.uuid
        return validated_data

    def get_user_info_from_kakao(self, kakao_user_info):
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
        birth_year = kakao_user_info['kakao_account'].get('birthyear')
        birthday = kakao_user_info['kakao_account'].get('birthday')
        if birth_year and birthday:
            birthday = datetime.datetime.strptime(f'{birth_year}-{birthday}', '%Y-%m%d')
        return {'name': name, 'phone_no': phone_no, 'sex': sex, 'birthday': birthday}


class AddressUserAssoc(s.ModelSerializer):
    address: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=cm.Address.objects.all(),
        write_only=True
    )
    user: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=get_user_model().objects.all(),
        write_only=True
    )
    large_area: s.Field = s.CharField(source='address.large_area')
    small_area: s.Field = s.CharField(source='address.small_area')

    class Meta:
        model = um.AddressUserAssoc
        exclude = ('id', 'created_at', 'uuid')


class PainAreaUserAssoc(s.ModelSerializer):
    name: s.Field = s.CharField(source='pain_area.name')

    class Meta:
        model = um.PainAreaUserAssoc
        exclude = ('id', 'pain_area', 'user', 'created_at', 'uuid')


@extend_schema_serializer(examples=sch.USER_DETAIL_EXAMPLE)
class User(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    username: s.Field = s.CharField(read_only=True)
    nickname: s.Field = s.CharField()
    name: s.Field = s.CharField(read_only=True)
    phone_no: s.Field = s.CharField()
    address: s.Field = cs.ReadWriteSerializerMethodField()
    birthday: s.Field = s.DateTimeField()
    sex: s.Field = s.CharField()
    pain_areas: s.Field = PainAreaUserAssoc(many=True, source='pain_area_user_assoc')
    is_real: s.Field = s.BooleanField(read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'username', 'nickname', 'birthday', 'phone_no', 'name',
                  'address', 'sex', 'is_real', 'pain_areas', 'created_at')

    def get_address(self, obj):
        qs = cm.Address.objects.filter(address_user_assoc__user=obj)
        if qs.exists():
            return {
                'large_area': qs.first().large_area,
                'small_area': qs.first().small_area
            }
        return {}

    def create(self, validated_data):
        user = validated_data['user']
        user.nickname = validated_data['nickname']
        user.birthday = validated_data['birthday']
        user.phone_no = validated_data['phone_no']
        user.sex = validated_data['sex']
        self.save_address(user, validated_data['address'])
        self.save_pain_areas(user, validated_data['pain_area_user_assoc'])

        user.save()
        return user

    def save_address(self, user, address):
        um.AddressUserAssoc.objects.filter(user=user).delete()

        address_qs = cm.Address.objects.filter(large_area=address['large_area'],
                                               small_area=address['small_area'])
        if not address_qs.exists():
            address = cm.Address.objects.create(large_area=address['large_area'],
                                                small_area=address['small_area'])
        else:
            address = address_qs.first()
        um.AddressUserAssoc.objects.create(user=user, address=address)

    def save_pain_areas(self, user, pain_area_user_assoc):
        um.PainAreaUserAssoc.objects.filter(user=user).delete()
        for area in pain_area_user_assoc:
            try:
                pain_area = um.PainArea.objects.get(name=area['pain_area']['name'])
                um.PainAreaUserAssoc.objects.create(user=user,
                                                    pain_area=pain_area)
            except um.PainArea.DoesNotExist:
                pass


class InsuranceUserAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    insurance: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        read_only=True
    )
    user: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        read_only=True
    )

    class Meta:
        model = um.InsuranceUserAssoc
        exclude = ('id', 'created_at')

    def create(self, validated_data):
        user = validated_data['user']
        self.send_insurance_consult_sms(user)
        return super().create(validated_data)

    def send_insurance_consult_sms(self, user):
        address_qs = cm.Address.objects.filter(address_user_assoc__user=user)
        if not address_qs.exists():
            raise exc.UserHasNoAddress()
        address = address_qs.first()
        message = f'{user.name}\n' \
                  f'{user.phone_no}\n' \
                  f'{user.birthday}\n' \
                  f'{user.sex}\n' \
                  f'{address.large_area} {address.small_area}'
        cu.send_sms(message)


@extend_schema_serializer(examples=sch.TOTAL_POINT_EXAMPLE)
class UserTotalPoint(s.Serializer):
    total_point: s.Field = s.IntegerField()


class UserPointHistory(s.ModelSerializer):
    user: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=get_user_model().objects.all(),
        write_only=True
    )
    modify_point: s.Field = s.IntegerField()
    content: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField()

    class Meta:
        model = um.UserPointHistory
        exclude = ('id', 'total_point', 'uuid')


class UserNotification(s.ModelSerializer):
    user: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=get_user_model().objects.all(),
        write_only=True
    )
    content: s.Field = s.CharField()
    is_new: s.Field = s.BooleanField()
    created_at: s.Field = s.DateTimeField()

    class Meta:
        model = um.UserPointHistory
        exclude = ('id', 'uuid')


class UserResignHistory(s.ModelSerializer):
    content: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField()

    class Meta:
        model = um.UserResignHistory
        exclude = ('id', 'username', 'uuid')

    def create(self, validated_data):
        user = validated_data['user']
        username = user.username
        instance = self.Meta.model.objects.save(username=username, content=validated_data['content'])
        user.resign()

        return instance


