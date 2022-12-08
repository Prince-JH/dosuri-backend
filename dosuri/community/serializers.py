from rest_framework import serializers as s

import dosuri.common.models
from dosuri.community import models as comm
from dosuri.common import models as cm
from dosuri.hospital import models as hm
from dosuri.user import models as um
from django.db import transaction

class AuthAttach(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    path: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.AuthAttach
        exclude = ('id', 'article_auth')

class ArticleAuth(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    sensitive_agreement: s.Field = s.BooleanField()
    personal_agreement: s.Field = s.BooleanField()
    status: s.Field = s.CharField(read_only=True)
    auth_attach: s.Field = AuthAttach(many=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAuth
        exclude = ('id', 'article')

class ArticleAttach(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    path: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAttach
        exclude = ('id', 'article')

class ArticleKeywordAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    keyword: s.Field = s.CharField(
        source='article_keyword.keyword',
        read_only=True
    )
    article_keyword: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        write_only=True,
        queryset=comm.ArticleKeyword.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleKeywordAssoc
        exclude = ('id', 'article')

class ArticleDetail(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    treatment_effect: s.Field = s.IntegerField(default=0)
    doctor_kindness: s.Field = s.IntegerField(default=0)
    therapist_kindness: s.Field = s.IntegerField(default=0)
    clean_score: s.Field = s.IntegerField(default=0)
    content: s.Field = s.CharField(read_only=False)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleDetail
        exclude = ('id', 'article')

class ArticleDoctorAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    doctor: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Doctor.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleDoctorAssoc
        exclude = ('id', 'article')

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
    article_attach = ArticleAttach(many=True)
    article_keyword_assoc = ArticleKeywordAssoc(many=True)
    article_detail = ArticleDetail(many=False)
    article_auth = ArticleAuth(many=False)
    article_doctor_assoc = ArticleDoctorAssoc(many=True)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')

    def create(self, validated_data):
        article_attach_list = validated_data.pop('article_attach')
        article_keyword_assoc_list = validated_data.pop('article_keyword_assoc')
        article_detail_data = validated_data.pop('article_detail')
        article_auth_data = validated_data.pop('article_auth')
        auth_attach_list = article_auth_data.pop('auth_attach')
        article_doctor_assoc_list = validated_data.pop('article_doctor_assoc')

        with transaction.atomic():
            article = comm.Article.objects.create(**validated_data)
            article_keyword_assoc_data = [comm.ArticleKeywordAssoc(**item, article=article) for item in article_keyword_assoc_list]
            comm.ArticleKeywordAssoc.objects.bulk_create(article_keyword_assoc_data)

            comm.ArticleDetail.objects.create(**article_detail_data, article=article)

            article_attach_data = [comm.ArticleAttach(**item, article=article) for item in article_attach_list]
            comm.ArticleAttach.objects.bulk_create(article_attach_data)

            article_auth = comm.ArticleAuth.objects.create(**article_auth_data, article=article)

            auth_attach_data = [comm.AuthAttach(**item, article_auth=article_auth) for item in auth_attach_list]
            comm.AuthAttach.objects.bulk_create(auth_attach_data)

            article_doctor_assoc_data = [comm.ArticleDoctorAssoc(**item, article=article) for item in doctor_assoc_list]
            comm.ArticleDoctorAssoc.objects.bulk_create(article_doctor_assoc_data)
        return article





class ArticleUpdate(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    status: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'article_type', 'cost', 'treat_count', 'user', 'hospital')
