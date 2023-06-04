from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers as s

from dosuri.hospital import (
    models as hm,
    model_managers as hmm,
    serializer_schemas as sch,
    constants as hc
)
from dosuri.common import (
    models as cm,
    utils as cu,
    geocoding as cg,
    tasks as ct,
)
from dosuri.community import (
    models as cmm,

)
from dosuri.user import (
    models as um
)
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema_field
from drf_spectacular.types import OpenApiTypes


class HospitalAttachmentAssoc(s.ModelSerializer):
    attachment: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=cm.Attachment.objects.all(),
        write_only=True
    )
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = hm.HospitalAttachmentAssoc
        exclude = ('uuid', 'id', 'hospital', 'created_at')

    @extend_schema_field(OpenApiTypes.STR)
    def get_signed_path(self, obj):
        return cu.generate_signed_path(obj.attachment)


class HospitalCalendar(s.ModelSerializer):
    monday: s.Field = s.CharField(allow_null=True)
    tuesday: s.Field = s.CharField(allow_null=True)
    wednesday: s.Field = s.CharField(allow_null=True)
    thursday: s.Field = s.CharField(allow_null=True)
    friday: s.Field = s.CharField(allow_null=True)
    saturday: s.Field = s.CharField(allow_null=True)
    sunday: s.Field = s.CharField(allow_null=True)

    class Meta:
        model = hm.HospitalCalendar
        exclude = ('uuid', 'id', 'hospital', 'created_at')


class HospitalKeyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    is_custom: s.Field = s.BooleanField(write_only=True)
    hospital: s.Field = s.CharField(read_only=True)

    class Meta:
        model = hm.HospitalKeyword
        exclude = ('id', 'created_at')


class HospitalKeywordAssoc(s.ModelSerializer):
    keyword: s.Field = s.CharField(source='keyword.name')

    class Meta:
        model = hm.HospitalKeywordAssoc
        exclude = ('id', 'uuid', 'hospital', 'created_at')


class PostHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()

    class Meta:
        model = hm.Hospital
        fields = ('uuid', 'name')

    def create(self, validated_data):
        validated_data['status'] = hc.HOSPITAL_PENDING
        hospital = super().create(validated_data)
        return hospital


class HospitalName(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField(read_only=True)

    class Meta:
        model = hm.Hospital
        fields = ('uuid', 'name')


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
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    calendar: s.Field = HospitalCalendar(write_only=True, source='hospital_calendar')
    keywords: s.Field = HospitalKeywordAssoc(write_only=True, many=True, source='hospital_keyword_assoc')
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    extra_fields = ['hospital_calendar', 'hospital_keyword_assoc', 'hospital_attachment_assoc']

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'status', 'code', 'last_updated_at', 'created_at')

    def create(self, validated_data):
        extra = {}
        for extra_field in self.extra_fields:
            extra[extra_field] = validated_data.pop(extra_field)
        hospital = super().create(validated_data)
        self.save_extra(hospital, **extra)
        return hospital

    def save_extra(self, hospital, **kwargs):
        if 'hospital_calendar' in kwargs:
            self.save_calendar(hospital, kwargs.pop('hospital_calendar'))
        if 'hospital_attachment_assoc' in kwargs:
            self.save_attachments(hospital, kwargs.pop('hospital_attachment_assoc'))
        if 'hospital_keyword_assoc' in kwargs:
            self.save_keywords(hospital, kwargs.pop('hospital_keyword_assoc'))
        return kwargs

    def save_calendar(self, hospital, calendar):
        hm.HospitalCalendar.objects.filter(hospital=hospital).delete()
        hm.HospitalCalendar.objects.create(hospital=hospital, **calendar)

    def save_attachments(self, hospital, assocs):
        hm.HospitalAttachmentAssoc.objects.filter(hospital=hospital).delete()
        for assoc in assocs:
            hm.HospitalAttachmentAssoc.objects.create(hospital=hospital, attachment=assoc['attachment'])

    def save_keywords(self, hospital, assocs):
        hm.HospitalKeywordAssoc.objects.filter(hospital=hospital).delete()
        for assoc in assocs:
            keyword = hm.HospitalKeyword.objects.get_or_create(name=assoc['keyword']['name'])
            hm.HospitalKeywordAssoc.objects.create(hospital=hospital, keyword=keyword)


class HospitalDetail(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(allow_null=True)
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(write_only=True, allow_null=True)
    calendar: s.Field = HospitalCalendar(source='hospital_calendar')
    keywords: s.Field = HospitalKeywordAssoc(many=True, source='hospital_keyword_assoc')
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    latitude: s.Field = s.FloatField()
    longitude: s.Field = s.FloatField()
    is_up: s.Field = s.BooleanField(read_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'status', 'code', 'last_updated_at', 'created_at')


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


class HospitalLatestArticleAvgPricePerHour(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    area: s.Field = s.CharField(allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    latest_article: s.Field = s.CharField(read_only=True, allow_null=True)
    latest_article_created_at: s.Field = s.CharField(read_only=True, allow_null=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    avg_price_per_hour: s.Field = s.FloatField(read_only=True, allow_null=True)

    class Meta:
        model = hm.Hospital
        fields = ['uuid', 'name', 'area', 'up_count', 'view_count', 'article_count', 'latest_article',
                  'latest_article_created_at', 'opened_at', 'avg_price_per_hour', 'attachments']


class DoctorKeyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    is_custom: s.Field = s.BooleanField(write_only=True)
    doctor: s.Field = s.CharField()

    class Meta:
        model = hm.DoctorKeyword
        exclude = ('id', 'created_at')


class DoctorKeywordAssoc(s.ModelSerializer):
    keyword: s.Field = s.CharField(source='keyword.name')

    class Meta:
        model = hm.DoctorKeywordAssoc
        exclude = ('uuid', 'id', 'doctor', 'created_at')


class DoctorDescription(s.ModelSerializer):
    description: s.Field = s.CharField()

    class Meta:
        model = hm.DoctorDescription
        exclude = ('uuid', 'id', 'doctor', 'created_at')


class DoctorAttachmentAssoc(s.ModelSerializer):
    attachment: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=cm.Attachment.objects.all(),
        write_only=True
    )
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = hm.DoctorAttachmentAssoc
        exclude = ('uuid', 'id', 'doctor', 'created_at')

    @extend_schema_field(OpenApiTypes.STR)
    def get_signed_path(self, obj):
        return cu.generate_signed_path(obj.attachment)


class Doctor(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    attachments: s.Field = DoctorAttachmentAssoc(many=True, source='doctor_attachment_assoc')
    name: s.Field = s.CharField()
    title: s.Field = s.CharField(allow_null=True)
    subtitle: s.Field = s.CharField(allow_null=True)
    position: s.Field = s.CharField(allow_null=True)
    descriptions: s.Field = DoctorDescription(many=True, source='doctor_detail')
    keywords: s.Field = DoctorKeywordAssoc(many=True, source='doctor_keyword_assoc')

    class Meta:
        model = hm.Doctor
        exclude = ('id', 'created_at')

    extra_fields = ['doctor_detail', 'doctor_keyword_assoc', 'doctor_attachment_assoc']

    def create(self, validated_data):
        extra = {}
        for extra_field in self.extra_fields:
            extra[extra_field] = validated_data.pop(extra_field)
        doctor = super().create(validated_data)
        self.save_extra(doctor, **extra)
        return doctor

    def save_extra(self, doctor, **kwargs):
        if 'doctor_detail' in kwargs:
            self.save_deatil(doctor, kwargs.pop('doctor_detail'))
        if 'doctor_attachment_assoc' in kwargs:
            self.save_attachments(doctor, kwargs.pop('doctor_attachment_assoc'))
        if 'doctor_keyword_assoc' in kwargs:
            self.save_keywords(doctor, kwargs.pop('doctor_keyword_assoc'))
        return kwargs

    def save_deatil(self, doctor, descriptions):
        hm.DoctorDescription.objects.filter(doctor=doctor).delete()
        for description in descriptions:
            hm.DoctorDescription.objects.create(doctor=doctor, description=description)

    def save_attachments(self, doctor, assocs):
        hm.DoctorAttachmentAssoc.objects.filter(doctor=doctor).delete()
        for assoc in assocs:
            hm.DoctorAttachmentAssoc.objects.create(doctor=doctor, attachment=assoc['attachment'])

    def save_keywords(self, doctor, assocs):
        hm.DoctorKeywordAssoc.objects.filter(doctor=doctor).delete()
        for assoc in assocs:
            keyword = hm.DoctorKeyword.objects.get_or_create(name=assoc['keyword']['name'])
            hm.DoctorKeywordAssoc.objects.create(doctor=doctor, keyword=keyword)


# @extend_schema_serializer(examples=sch.HOSPITAL_TREATMENT_EXAMPLE)
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


class HospitalReservation(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    user: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        read_only=True
    )

    class Meta:
        model = hm.HospitalReservation
        exclude = ('id', 'created_at')

    def create(self, validated_data):
        hospital = validated_data['hospital']
        user = validated_data['user']
        qs = self.Meta.model.objects.filter(hospital=hospital, user=user,
                                            created_at__gte=timezone.now() - timedelta(days=1))
        if qs.exists():
            return qs.first()
        message = self.make_message(hospital, user)
        ct.announce_hospital_reservation.delay(message)
        return super().create(validated_data)

    def make_message(self, hospital, user):
        message = f'병원 예약 신청\n' \
                  f'{hospital.name}\n ' \
                  f'{hospital.phone_no}\n' \
                  f'\n' \
                  f'{user.name} {user.sex}\n' \
                  f'{user.phone_no}\n' \
                  f'{user.birthday.strftime("%Y/%m/%d")}\n'
        return message


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
    is_partner: s.Field = s.BooleanField(read_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'status', 'code', 'last_updated_at', 'created_at')


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
    is_partner: s.Field = s.BooleanField(read_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'status', 'code', 'last_updated_at', 'created_at')


class GoodPriceHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    area: s.Field = s.CharField(allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    is_partner: s.Field = s.BooleanField(read_only=True)
    article_count: s.Field = s.IntegerField(read_only=True)
    avg_price_per_hour: s.Field = s.FloatField(read_only=True, allow_null=True)
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')

    class Meta:
        model = hm.Hospital
        fields = ['uuid', 'name', 'area', 'up_count', 'view_count', 'article_count', 'avg_price_per_hour', 'is_partner',
                  'attachments']


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
    is_partner: s.Field = s.BooleanField(read_only=True)
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    distance: s.Field = s.FloatField(read_only=True, allow_null=True)
    attachments: s.Field = HospitalAttachmentAssoc(many=True, source='hospital_attachment_assoc')
    latitude: s.Field = s.FloatField(write_only=True)
    longitude: s.Field = s.FloatField(write_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id', 'status', 'code', 'last_updated_at', 'created_at')


@extend_schema_serializer(examples=sch.HOME_HOSPITAL_EXAMPLE)
class HomeHospital(s.Serializer):
    address: s.Field = s.CharField()
    top_hospitals: s.Field = s.ListField()
    new_hospitals: s.Field = s.ListField()
    good_price_hospitals: s.Field = s.ListField()
    many_review_hospitals: s.Field = s.ListField()
    new_review_hospitals: s.Field = s.ListField()
