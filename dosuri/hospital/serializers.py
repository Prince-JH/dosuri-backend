from rest_framework import serializers as s

from dosuri.hospital import models as hm
from dosuri.common import models as cm
from dosuri.community import (
    models as cmm,
)


class Hospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_null=True)
    area: s.Field = s.CharField(allow_null=True)
    phone_no: s.Field = s.CharField(allow_null=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    article_count: s.Field = s.SerializerMethodField()
    latest_article: s.Field = s.SerializerMethodField(allow_null=True)
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    def get_article_count(self, obj):
        return cmm.Article.objects.filter(hospital=obj).count()

    def get_latest_article(self, obj):
        latest_article = cmm.ArticleDetail.objects.filter(article__hospital=obj).order_by('-created_at').first()
        if not latest_article:
            return
        return latest_article.content

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
        exclude = ('id', 'title')


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
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalAddressAssoc
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
    price_per_hour: s.Field = s.IntegerField()
    description: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = hm.HospitalTreatment
        exclude = ('id',)


class TopHospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.CharField()
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
