from datetime import datetime, timedelta

from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    models as um,
    constants as uc,
    serializer_schemas as sch,
    exceptions as uexc,
    utils as uu,
)
from dosuri.common import (
    models as cm,
    serializers as cs,
    utils as cu,
    tasks as ct,
)


@extend_schema_serializer(examples=sch.AUTH_EXAMPLE)
class Auth(s.Serializer):
    user_uuid: s.Field = s.CharField(read_only=True)
    username: s.Field = s.CharField(write_only=True, required=False)
    password: s.Field = s.CharField(write_only=True, required=False)
    token: s.Field = s.CharField(write_only=True, required=False)
    type: s.Field = s.CharField(write_only=True)
    access_token: s.Field = s.CharField(read_only=True)
    refresh_token: s.Field = s.CharField(read_only=True)
    is_new: s.Field = s.BooleanField(read_only=True)

    def create(self, validated_data):
        auth_type = validated_data['type']

        origin = self.context['request'].build_absolute_uri()

        if auth_type == uc.AUTH_PASSWORD:
            username = validated_data['username']
            password = validated_data['password']
            qs = um.User.objects.filter(username=username, password=password)
            if not qs.exists():
                raise uexc.WrongUsernameOrPasswordException()
            user = qs.first()
            user_info = {}

        else:
            token = validated_data.get('token')
            if not token:
                raise uexc.RequireTokenException()

            if auth_type == uc.AUTH_KAKAO:
                auth = a.KaKaoAuth(token, origin)

            elif auth_type == uc.AUTH_GOOGLE:
                auth = a.GoogleAuth(token, origin)

            user_info = auth.get_user_info()
            username = user_info['username']
            user = um.User.objects.get_or_create(username=username)[0]

        is_new = user.is_new()
        if is_new:
            user_info['nickname'] = uu.get_random_nickname()
            um.User.objects.update_user_info(user, user_info)

        tokens = a.get_tokens_for_user(user)

        validated_data['access_token'] = tokens['access']
        validated_data['refresh_token'] = tokens['refresh']
        validated_data['is_new'] = is_new
        validated_data['user_uuid'] = user.uuid
        return validated_data


class AuthV2(s.Serializer):
    code: s.Field = s.CharField(write_only=True, required=False)
    token: s.Field = s.CharField(read_only=True, required=False)
    type: s.Field = s.CharField(write_only=True)

    def create(self, validated_data):
        auth_type = validated_data['type']

        origin = self.context['request'].build_absolute_uri()

        if auth_type == uc.AUTH_APPLE:
            pass

        validated_data['token'] = ''
        return validated_data


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


class UserNotice(s.ModelSerializer):
    unread_notice: s.Field = s.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('unread_notice',)

    def update(self, instance, validated_data):
        instance.unread_notice = False
        instance.save()
        return instance


@extend_schema_serializer(examples=sch.USER_DETAIL_EXAMPLE)
class User(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    username: s.Field = s.CharField(read_only=True)
    nickname: s.Field = s.CharField()
    name: s.Field = s.CharField(allow_blank=True, allow_null=True)
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
                  'address', 'sex', 'is_real', 'pain_areas', 'created_at', 'unread_notice')

    def create(self, validated_data):
        user = get_user_model().objects.create()
        return self.save_user_info(user, validated_data)

    def update(self, instance, validated_data):
        user = instance
        return self.save_user_info(user, validated_data)

    def get_address(self, obj):
        address = um.UserAddress.objects.get_main_address(user=obj)
        if address:
            return {'name': address.name, 'address': address.address, 'address_type': address.address_type,
                    'latitude': address.latitude, 'longitude': address.longitude}
        return None

    def save_user_info(self, user, info_data):
        info_data = self.save_extra(user, **info_data)
        for key, value in info_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save()
        return user

    def save_extra(self, user, **kwargs):
        if 'address' in kwargs:
            self.save_address(user, kwargs.pop('address'))

        if 'pain_area_user_assoc' in kwargs:
            self.save_pain_areas(user, kwargs.pop('pain_area_user_assoc'))
        return kwargs

    def save_address(self, user, address_data):
        qs = um.UserAddress.objects.filter(user=user, name=address_data['name'])
        if qs.exists():
            return
        address_data.update({'user': user})
        address = um.UserAddress.objects.create_address(address_data)
        um.UserAddress.objects.set_main_address(address)
        return address

    def save_pain_areas(self, user, pain_area_user_assoc):
        um.PainAreaUserAssoc.objects.filter(user=user).delete()
        for area in pain_area_user_assoc:
            try:
                pain_area = um.PainArea.objects.get(name=area['pain_area']['name'])
                um.PainAreaUserAssoc.objects.create(user=user,
                                                    pain_area=pain_area)
            except um.PainArea.DoesNotExist:
                pass


class UserToken(s.Serializer):
    username: s.Field = s.CharField(write_only=True)
    access: s.Field = s.CharField(read_only=True)
    refresh: s.Field = s.CharField(read_only=True)


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
        insurance = validated_data['insurance']
        user = validated_data['user']
        qs = self.Meta.model.objects.filter(insurance=insurance, user=user,
                                            created_at__gte=timezone.now() - timedelta(days=1))
        if qs.exists():
            return qs.first()
        message = self.make_message(user)
        ct.announce_insurance_consult.delay(message)
        if user.phone_no:
            ct.announce_insurance_consult_to_user.delay(user.phone_no)
        return super().create(validated_data)

    def make_message(self, user):
        address_qs = um.UserAddress.objects.filter(user=user, address_type=uc.ADDRESS_HOME)
        if not address_qs.exists():
            address_qs = um.UserAddress.objects.filter(user=user, is_main=True)
            if not address_qs.exists():
                raise uexc.UserHasNoAddress()
        address = address_qs.first().address.split(' ')
        message = f'새로운 보험 신청\n' \
                  f'{user.name} ({user.sex})\n' \
                  f'{user.phone_no}\n' \
                  f'{user.birthday.strftime("%Y/%m/%d")}\n' \
                  f'{address[0]} {address[1]}'
        return message


@extend_schema_serializer(examples=sch.TOTAL_POINT_EXAMPLE)
class UserTotalPoint(s.Serializer):
    total_point: s.Field = s.IntegerField()


class UserPointHistory(s.ModelSerializer):
    modify_point: s.Field = s.IntegerField()
    content: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = um.UserPointHistory
        exclude = ('id', 'user', 'total_point', 'uuid')


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
    reason: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = um.UserResignHistory
        exclude = ('id', 'username', 'uuid')

    def create(self, validated_data):
        user = validated_data['user']
        username = user.username
        instance = self.Meta.model.objects.create(username=username, reason=validated_data['reason'])
        user.resign()

        return instance


@extend_schema_serializer(examples=sch.USER_ADDRESS_EXAMPLE)
class UserAddress(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField(allow_null=True)
    address: s.Field = s.CharField()
    address_type: s.Field = s.ChoiceField(choices=[uc.ADDRESS_HOME, uc.ADDRESS_OFFICE, uc.ADDRESS_ETC])
    is_main: s.Field = s.BooleanField(read_only=True)
    latitude: s.Field = s.FloatField()
    longitude: s.Field = s.FloatField()

    class Meta:
        model = um.UserAddress
        exclude = ('id', 'user', 'created_at')

    def create(self, validated_data):
        return self.Meta.model.objects.create_address(validated_data)


class UserAddressDetail(s.ModelSerializer):
    is_main: s.Field = s.BooleanField()

    class Meta:
        model = um.UserAddress
        fields = ('is_main',)

    def update(self, instance, validated_data):
        if validated_data.get('is_main'):
            self.Meta.model.objects.set_main_address(instance)
        return super().update(instance, validated_data)
