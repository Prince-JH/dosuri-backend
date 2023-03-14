from datetime import datetime, timedelta

from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers as s

from dosuri.user import (
    auth as a,
    models as um,
    constants as c,
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

        if auth_type == c.AUTH_PASSWORD:
            username = validated_data['username']
            password = validated_data['password']
            qs = um.User.objects.filter(username=username, password=password)
            if not qs.exists():
                raise uexc.WrongUsernameOrPasswordException()
            user = qs.first()
            user_info = {}

        elif auth_type == c.AUTH_KAKAO:
            token = validated_data.get('token')
            if not token:
                raise uexc.RequireTokenException()
            auth_factory = a.KaKaoAuth(token, origin)
            kakao_user_info = auth_factory.authenticate()
            username = kakao_user_info['kakao_account']['email']

            user = um.User.objects.get_or_create(username=username)[0]
            user_info = self.get_user_info_from_kakao(kakao_user_info)

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
            phone_no = '0' + phone_no
        birth_year = kakao_user_info['kakao_account'].get('birthyear')
        birthday = kakao_user_info['kakao_account'].get('birthday')
        if birth_year and birthday:
            birthday = datetime.strptime(f'{birth_year}-{birthday}', '%Y-%m%d').astimezone()
        else:
            birthday = None
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
        return self.save_user_info(user, validated_data)

    def update(self, instance, validated_data):
        user = instance
        return self.save_user_info(user, validated_data)

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
        address_qs = cm.Address.objects.filter(address_user_assoc__user=user)
        if not address_qs.exists():
            raise uexc.UserHasNoAddress()
        address = address_qs.first()
        message = f'새로운 보험 신청\n' \
                  f'{user.name} ({user.sex})\n' \
                  f'{user.phone_no}\n' \
                  f'{user.birthday.strftime("%Y/%m/%d")}\n' \
                  f'{address.large_area} {address.small_area}'
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


class UserAddress(s.ModelSerializer):
    uuid: s.Field = s.CharField()
    reason: s.Field = s.CharField()
    reason: s.Field = s.CharField()
    reason: s.Field = s.CharField()

    class Meta:
        model = um.UserAddress
        exclude = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = validated_data['user']
        username = user.username
        instance = self.Meta.model.objects.create(username=username, reason=validated_data['reason'])
        user.resign()

        return instance
