from rest_framework import serializers as s

import dosuri.common.models
from dosuri.community import models as comm
from dosuri.community import constants as cc
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
    status: s.Field = s.CharField(required=False)
    auth_attach: s.Field = AuthAttach(many=True, required=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAuth
        exclude = ('id', 'article')
    def update(self, instance, validated_data):
        instance.sensitive_agreement = validated_data.get('sensitive_agreement', instance.sensitive_agreement)
        instance.personal_agreement = validated_data.get('personal_agreement', instance.personal_agreement)
        if validated_data.get('status', instance.status) in [cc.STATUS_DENY, cc.STATUS_COMPLETE]:
            with transaction.atomic():
                instance.status = validated_data.get('status', instance.status)
                instance.article.status=validated_data.get('status', instance.status)
                instance.save()
                instance.article.save()
        return instance


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
    staff_kindness: s.Field = s.IntegerField(default=0)
    clean_score: s.Field = s.IntegerField(default=0)
    created_at: s.Field = s.DateTimeField(read_only=True)
    cost: s.Field = s.IntegerField(default=None, required=False)
    treat_count: s.Field = s.IntegerField(default=None, required=False)

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
    content: s.Field = s.CharField(read_only=False)
    article_attach = ArticleAttach(many=True, write_only=True, required=False)
    article_keyword_assoc = ArticleKeywordAssoc(many=True, write_only=True, required=True)
    article_detail = ArticleDetail(many=False, write_only=True, required=False)
    article_auth = ArticleAuth(many=False, write_only=True, required=False)
    article_doctor_assoc = ArticleDoctorAssoc(many=True, write_only=True, required=False)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')

    def create(self, validated_data):
        if 'article_attach' in validated_data:
            article_attach_list = validated_data.pop('article_attach')
        else:
            article_attach_list = False
            
        if "article_detail" in validated_data:
            article_detail_data = validated_data.pop('article_detail')
        else:
            article_detail_data = False

        if "article_doctor_assoc" in validated_data:
            article_doctor_assoc_list = validated_data.pop('article_doctor_assoc')
        else:
            article_doctor_assoc_list = False

        article_keyword_assoc_list = validated_data.pop('article_keyword_assoc')
        if 'article_auth' in validated_data:
            article_auth_data = validated_data.pop('article_auth')
            auth_attach_list = article_auth_data.pop('auth_attach')
        else:
            article_auth_data = False

        if validated_data['article_type'] == cc.ARTICLE_REVIEW:
            with transaction.atomic():
                article = comm.Article.objects.create(**validated_data)
                article_keyword_assoc_data = [comm.ArticleKeywordAssoc(**item, article=article) for item in
                                            article_keyword_assoc_list]
                comm.ArticleKeywordAssoc.objects.bulk_create(article_keyword_assoc_data)
                if article_detail_data:
                    comm.ArticleDetail.objects.create(**article_detail_data, article=article)
                if article_attach_list:
                    article_attach_data = [comm.ArticleAttach(**item, article=article) for item in article_attach_list]
                    comm.ArticleAttach.objects.bulk_create(article_attach_data)

                if article_auth_data:
                    article_auth = comm.ArticleAuth.objects.create(**article_auth_data, article=article)
                    auth_attach_data = [comm.AuthAttach(**item, article_auth=article_auth) for item in auth_attach_list]
                    comm.AuthAttach.objects.bulk_create(auth_attach_data)

                if article_doctor_assoc_list:
                    article_doctor_assoc_data = [comm.ArticleDoctorAssoc(**item, article=article) for item in article_doctor_assoc_list]
                    comm.ArticleDoctorAssoc.objects.bulk_create(article_doctor_assoc_data)
        if validated_data['article_type'] == cc.ARTICLE_QUESTION:
            with transaction.atomic():
                article = comm.Article.objects.create(**validated_data)
                
                if article_attach_list:
                    article_attach_data = [comm.ArticleAttach(**item, article=article) for item in article_attach_list]
                    comm.ArticleAttach.objects.bulk_create(article_attach_data)
        return article


