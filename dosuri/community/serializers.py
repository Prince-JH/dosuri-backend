from rest_framework import serializers as s

import dosuri.common.models
from dosuri.community import models as comm
from dosuri.common import models as cm
from dosuri.hospital import models as hm
from dosuri.user import models as um

class Article(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user: s.Field = s.SlugRelatedField(
        read_only=True,
        slug_field='uuid',
        # queryset=um.User.objects.all()
    )
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=hm.Hospital.objects.all()
    )

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')


class ArticleAttach(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    path: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAttach
        exclude = ('id',)


class DoctorAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Doctor.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.DoctorAssoc
        exclude = ('id',)


class ArticleKeywordAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    article_keyword: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.HospitalTreatment.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleKeywordAssoc
        exclude = ('id',)


class ArticleDetail(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    treatment_effect: s.Field = s.IntegerField(default=0)
    doctor_kindness: s.Field = s.IntegerField(default=0)
    therapist_kindness: s.Field = s.IntegerField(default=0)
    clean_score: s.Field = s.IntegerField(default=0)
    content: s.Field = s.CharField(read_only=False)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleDetail
        exclude = ('id',)


class ArticleAuth(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    sensitive_agreement: s.Field = s.BooleanField()
    personal_agreement: s.Field = s.BooleanField()
    status: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAuth
        exclude = ('id',)


class AuthAttach(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article_auth: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.ArticleAuth.objects.all()
    )
    path: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.AuthAttach
        exclude = ('id',)


class ArticleUpdate(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    status: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'article_type', 'cost', 'treat_count', 'user', 'hospital')
