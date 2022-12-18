from rest_framework import serializers as s

from dosuri.hospital import (
    models as hm,
    model_managers as hmm
)
from dosuri.common import models as cm
from dosuri.community import (
    models as cmm,
)


class HospitalImage(s.ModelSerializer):
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all(),
        write_only=True
    )
    url: s.Field = s.CharField()

    class Meta:
        model = hm.HospitalImage
        exclude = ('uuid', 'id', 'title', 'created_at')


class Hospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(write_only=True, allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(write_only=True, allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    images = HospitalImage(many=True, source='hospital_image')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'code')


class HospitalCalendar(s.ModelSerializer):
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all(),
        write_only=True
    )
    monday: s.Field = s.CharField(allow_null=True)
    tuesday: s.Field = s.CharField(allow_null=True)
    wednesday: s.Field = s.CharField(allow_null=True)
    thursday: s.Field = s.CharField(allow_null=True)
    friday: s.Field = s.CharField(allow_null=True)
    saturday: s.Field = s.CharField(allow_null=True)
    sunday: s.Field = s.CharField(allow_null=True)

    class Meta:
        model = hm.HospitalCalendar
        exclude = ('uuid', 'id', 'created_at')


class HospitalKeyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    is_custom: s.Field = s.BooleanField(write_only=True)
    hospital: s.Field = s.CharField(read_only=True)

    class Meta:
        model = hm.HospitalKeyword
        exclude = ('id', 'created_at')


class HospitalKeywordAssoc(s.ModelSerializer):
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all(),
        write_only=True
    )
    # keyword: s.Field = s.SlugRelatedField(
    #     slug_field='uuid',
    #     queryset=hm.HospitalKeyword.objects.all()
    # )
    keyword: s.Field = s.CharField(source='keyword.name')

    class Meta:
        model = hm.HospitalKeywordAssoc
        exclude = ('id', 'created_at', 'uuid')


class HospitalDetail(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(write_only=True, allow_null=True)
    calendar: s.Field = HospitalCalendar(source='hospital_calendar')
    keywords: s.Field = HospitalKeywordAssoc(many=True, source='hospital_keyword_assoc')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)
    is_up: s.Field = s.BooleanField(read_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'view_count', 'code')


class HospitalAddressAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    address: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=cm.Address.objects.all()
    )

    class Meta:
        model = hm.HospitalAddressAssoc
        exclude = ('id', 'created_at')


class DoctorKeyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    is_custom: s.Field = s.BooleanField(write_only=True)
    doctor: s.Field = s.CharField()

    class Meta:
        model = hm.DoctorKeyword
        exclude = ('id', 'created_at')


class DoctorKeywordAssoc(s.ModelSerializer):
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Doctor.objects.all(),
        write_only=True
    )
    keyword: s.Field = s.CharField(source='keyword.name')

    class Meta:
        model = hm.DoctorKeywordAssoc
        exclude = ('uuid', 'id', 'created_at')


class DoctorDescription(s.ModelSerializer):
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Doctor.objects.all(),
        write_only=True
    )
    description: s.Field = s.CharField()

    class Meta:
        model = hm.DoctorDescription
        fields = ('doctor', 'description')


class Doctor(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    thumbnail_url: s.Field = s.CharField(allow_null=True)
    name: s.Field = s.CharField()
    title: s.Field = s.CharField(allow_null=True)
    subtitle: s.Field = s.CharField(allow_null=True)
    position: s.Field = s.CharField(allow_null=True)
    descriptions: s.Field = DoctorDescription(many=True, source='doctor_detail')
    # keywords: s.Field = s.ListField(read_only=True)
    keywords: s.Field = DoctorKeywordAssoc(many=True, source='doctor_keyword_assoc')

    class Meta:
        model = hm.Doctor
        exclude = ('id', 'created_at')


class HospitalTreatment(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    price: s.Field = s.IntegerField()
    price_per_hour: s.Field = s.IntegerField(allow_null=True)
    description: s.Field = s.CharField(allow_null=True)

    class Meta:
        model = hm.HospitalTreatment
        exclude = ('id', 'created_at')


class HomeHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(allow_null=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at')


class HospitalUserAssoc(s.ModelSerializer):
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    is_up: s.Field = s.BooleanField()

    class Meta:
        model = hm.HospitalUserAssoc
        exclude = ('id', 'user', 'created_at')

    def create(self, validated_data):
        hospital = validated_data['hospital']
        user = validated_data['user']
        is_up = validated_data['is_up']
        self.Meta.model.objects.press_up_button(hospital, user, is_up)
        return {'hospital': hospital, 'is_up': is_up}


class HospitalSearch(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    word: s.Field = s.CharField()

    class Meta:
        model = hm.HospitalSearch
        exclude = ('id', 'user', 'created_at')


class AroundHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(write_only=True, allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(write_only=True, allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    images = HospitalImage(many=True, source='hospital_image')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'code')


class NewHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(write_only=True, allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(write_only=True, allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    images = HospitalImage(many=True, source='hospital_image')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'code')


class GoodPriceHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(write_only=True, allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(write_only=True, allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    images = HospitalImage(many=True, source='hospital_image')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'code')


class GoodReviewHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(write_only=True, allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(write_only=True, allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    is_partner: s.Field = s.BooleanField(write_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    images = HospitalImage(many=True, source='hospital_image')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'created_at', 'code')


class HomeHospital(s.Serializer):
    top_hospitals: s.Field = s.ListField()
    new_hospitals: s.Field = s.ListField()
    good_price_hospitals: s.Field = s.ListField()
    good_review_hospitals: s.Field = s.ListField()
