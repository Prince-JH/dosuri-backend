from rest_framework import serializers as s

import dosuri.common.models
from dosuri.hospital import models as hm
from dosuri.common import models as cm


class Address(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    do: s.Field = s.CharField(allow_null=True)
    city: s.Field = s.CharField(allow_null=True)
    gun: s.Field = s.CharField(allow_null=True)
    gu: s.Field = s.CharField(allow_null=True)
    street: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.common.models.Address
        exclude = ('id',)


class Hospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=cm.Address.objects.all()
    )
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.Hospital
        exclude = ('id',)


class HospitalImage(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    url: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalImage
        exclude = ('id',)


class HospitalCalendar(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    monday: s.Field = s.CharField(allow_null=True)
    tuesday: s.Field = s.CharField(allow_null=True)
    wednesday: s.Field = s.CharField(allow_null=True)
    thursday: s.Field = s.CharField(allow_null=True)
    friday: s.Field = s.CharField(allow_null=True)
    saturday: s.Field = s.CharField(allow_null=True)
    sunday: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalCalendar
        exclude = ('id',)


class Doctor(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    thumbnail_url: s.Field = s.CharField(allow_null=True)
    name: s.Field = s.CharField()
    title: s.Field = s.CharField(allow_null=True)
    position: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.Doctor
        exclude = ('id',)


class DoctorDescription(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Doctor.objects.all()
    )
    description: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.DoctorDescription
        exclude = ('id',)


class Keyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    is_custom: s.Field = s.BooleanField()
    domain: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.Keyword
        exclude = ('id',)


class HospitalKeywordAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    keyword: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Keyword.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalKeywordAssoc
        exclude = ('id',)


class DoctorKeywordAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Doctor.objects.all()
    )
    keyword: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Keyword.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.DoctorKeywordAssoc
        exclude = ('id',)


class HospitalTreatment(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    name: s.Field = s.CharField()
    hospital: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )
    price: s.Field = s.IntegerField()
    duration: s.Field = s.IntegerField()
    description: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalTreatment
        exclude = ('id',)
