from django.contrib.auth import get_user_model
from rest_framework import serializers as s

import dosuri.common.models
from dosuri.community import models as comm
from dosuri.community import constants as cc
from dosuri.common import models as cm
from dosuri.hospital import models as hm
from dosuri.user import models as um
from django.db import transaction
from dosuri.common import serializers as cs
from datetime import datetime
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class CommunityUser(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    nickname: s.Field = s.CharField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['uuid', 'nickname']

# class AuthAttach(s.ModelSerializer):
#     uuid: s.Field = s.CharField(read_only=True)
#     path: s.Field = s.CharField()
#     created_at: s.Field = s.DateTimeField(read_only=True)

#     class Meta:
#         model = dosuri.community.models.AuthAttach
#         exclude = ('id', 'article_auth')
class GetArticleAttachmentAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    attachment: s.Field = cs.Attachment(read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAttachmentAssoc
        exclude = ('id', 'article')

class ArticleAttachmentAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    attachment: s.Field = s.SlugRelatedField(
        read_only=False,
        slug_field='uuid',
        queryset=cm.Attachment.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAttachmentAssoc
        exclude = ('id', 'article')
    def to_representation(self, obj):
        self.fields['attachment'] = cs.PutAttachment(read_only=True)
        return super().to_representation(obj)

class AuthAttachmentAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    attachment: s.Field = s.SlugRelatedField(
        read_only=False,
        slug_field='uuid',
        queryset=cm.Attachment.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.AuthAttachmentAssoc
        exclude = ('id', 'article_auth')

    def to_representation(self, obj):
        self.fields['attachment'] = cs.PutAttachment(read_only=True)
        return super().to_representation(obj)

class ArticleAuth(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    sensitive_agreement: s.Field = s.BooleanField()
    personal_agreement: s.Field = s.BooleanField()
    status: s.Field = s.CharField(required=False)
    auth_attachment_assoc: s.Field = AuthAttachmentAssoc(many=True)
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


# class ArticleAttach(s.ModelSerializer):
#     uuid: s.Field = s.CharField(read_only=True)
#     path: s.Field = s.CharField()
#     created_at: s.Field = s.DateTimeField(read_only=True)

#     class Meta:
#         model = dosuri.community.models.ArticleAttach
#         exclude = ('id', 'article')




class ArticleKeywordAssoc(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    keyword: s.Field = s.CharField(
        source='treatment_keyword.keyword',
        read_only=True
    )
    treatment_keyword: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        write_only=True,
        queryset=comm.TreatmentKeyword.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleKeywordAssoc
        exclude = ('id', 'article')


class ArticleDetailSer(s.ModelSerializer):
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

class PostArticleThread(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    content: s.Field = s.CharField()
    article_comment: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=comm.ArticleComment.objects.all()
    )
    created_at: s.Field = s.DateTimeField(read_only=True)
    created_at: s.Field = s.SerializerMethodField()
    mention_user: s.Field = s.SlugRelatedField(
        read_only=False,
        slug_field='uuid',
        queryset=um.User.objects.all()
    )

    class Meta:
        model = dosuri.community.models.ArticleThread
        exclude = ('id',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, instance): ## 준호님의 요청으로 created_at을 XX분/시간/일/월/년 전으로 대체하는 로직 추후 작업시 MethodField를 DatatimeField로 변환 요망
        now = datetime.now().astimezone()
        created_at = instance.created_at
        total_seconds = (now-created_at).total_seconds()
        if total_seconds < 60:
            created_at = str(int(total_seconds))+ '초 전'
        elif total_seconds/60 < 60:
            created_at = str(int(total_seconds/60))+ '분 전'
        elif total_seconds/3600 < 24:
            created_at = str(int(total_seconds/3600))+ '시간 전'
        elif (total_seconds/3600)/24 < 30:
            created_at = str(int((total_seconds/3600)/24))+ '일 전'
        elif ((total_seconds/3600)/24)/30 < 12:
            created_at = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
        else:
            created_at = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return created_at

class ArticleThread(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    content: s.Field = s.CharField()
    article_comment: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=comm.ArticleComment.objects.all()
    )
    # created_at: s.Field = s.DateTimeField(read_only=True)
    created_at: s.Field = s.SerializerMethodField()
    mention_user: s.Field = CommunityUser(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleThread
        exclude = ('id',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, instance): ## 준호님의 요청으로 created_at을 XX분/시간/일/월/년 전으로 대체하는 로직 추후 작업시 MethodField를 DatatimeField로 변환 요망
        now = datetime.now().astimezone()
        created_at = instance.created_at
        total_seconds = (now-created_at).total_seconds()
        if total_seconds < 60:
            created_at = str(int(total_seconds))+ '초 전'
        elif total_seconds/60 < 60:
            created_at = str(int(total_seconds/60))+ '분 전'
        elif total_seconds/3600 < 24:
            created_at = str(int(total_seconds/3600))+ '시간 전'
        elif (total_seconds/3600)/24 < 30:
            created_at = str(int((total_seconds/3600)/24))+ '일 전'
        elif ((total_seconds/3600)/24)/30 < 12:
            created_at = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
        else:
            created_at = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return created_at

class ArticleComment(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    content: s.Field = s.CharField()
    article_thread = ArticleThread(many=True, read_only=True)
    article: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    # created_at: s.Field = s.DateTimeField(read_only=True)
    created_at: s.Field = s.SerializerMethodField()

    class Meta:
        model = dosuri.community.models.ArticleComment
        exclude = ('id',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, instance): ## 준호님의 요청으로 created_at을 XX분/시간/일/월/년 전으로 대체하는 로직 추후 작업시 MethodField를 DatatimeField로 변환 요망
        now = datetime.now().astimezone()
        created_at = instance.created_at
        total_seconds = (now-created_at).total_seconds()
        if total_seconds < 60:
            created_at = str(int(total_seconds))+ '초 전'
        elif total_seconds/60 < 60:
            created_at = str(int(total_seconds/60))+ '분 전'
        elif total_seconds/3600 < 24:
            created_at = str(int(total_seconds/3600))+ '시간 전'
        elif (total_seconds/3600)/24 < 30:
            created_at = str(int((total_seconds/3600)/24))+ '일 전'
        elif ((total_seconds/3600)/24)/30 < 12:
            created_at = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
        else:
            created_at = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return created_at

class Article(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    article_type: s.Field = s.CharField()
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    created_at: s.Field = s.DateTimeField(read_only=True)
    hospital: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=hm.Hospital.objects.all(),
        required=False
    )
    content: s.Field = s.CharField(read_only=False)
    article_attachment_assoc: s.Field = ArticleAttachmentAssoc(many=True, write_only=True)
    article_keyword_assoc = ArticleKeywordAssoc(many=True, write_only=True, required=False)
    article_detail = ArticleDetailSer(many=False, write_only=True, required=False)
    article_auth = ArticleAuth(many=False, write_only=True, required=False)
    article_doctor_assoc = ArticleDoctorAssoc(many=True, write_only=True, required=False)
    is_like: s.Field = s.SerializerMethodField(read_only=True)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')
    def create(self, validated_data):
        if 'article_attachment_assoc' in validated_data:
            attachment_assoc_list = validated_data.pop('article_attachment_assoc')
        else:
            attachment_assoc_list = False

        if "article_detail" in validated_data:
            article_detail_data = validated_data.pop('article_detail')
        else:
            article_detail_data = False

        if "article_doctor_assoc" in validated_data:
            article_doctor_assoc_list = validated_data.pop('article_doctor_assoc')
        else:
            article_doctor_assoc_list = False

        if 'article_auth' in validated_data:
            article_auth_data = validated_data.pop('article_auth')
            auth_attachment_list = article_auth_data.pop('auth_attachment_assoc')
        else:
            article_auth_data = False

        if validated_data['article_type'] == cc.ARTICLE_REVIEW:
            article_keyword_assoc_list = validated_data.pop('article_keyword_assoc')
            with transaction.atomic():
                article = comm.Article.objects.create(**validated_data)
                article_keyword_assoc_data = [comm.ArticleKeywordAssoc(**item, article=article) for item in
                                            article_keyword_assoc_list]
                comm.ArticleKeywordAssoc.objects.bulk_create(article_keyword_assoc_data)
                if article_detail_data:
                    comm.ArticleDetail.objects.create(**article_detail_data, article=article)
                if attachment_assoc_list:
                    article_attachment_assoc_data = [comm.ArticleAttachmentAssoc(**item, article=article) for item in attachment_assoc_list]
                    comm.ArticleAttachmentAssoc.objects.bulk_create(article_attachment_assoc_data)
                if article_auth_data:
                    article_auth = comm.ArticleAuth.objects.create(**article_auth_data, article=article)
                    auth_attachment_assoc_data = [comm.AuthAttachmentAssoc(**item, article_auth=article_auth) for item in auth_attachment_list]
                    comm.AuthAttachmentAssoc.objects.bulk_create(auth_attachment_assoc_data)

                if article_doctor_assoc_list:
                    article_doctor_assoc_data = [comm.ArticleDoctorAssoc(**item, article=article) for item in article_doctor_assoc_list]
                    comm.ArticleDoctorAssoc.objects.bulk_create(article_doctor_assoc_data)
        if validated_data['article_type'] == cc.ARTICLE_QUESTION:
            with transaction.atomic():
                article = comm.Article.objects.create(**validated_data)

        return article

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_like(self, instance):
        return comm.ArticleLike.objects.filter(article=instance,
            user=self.context['request'].user
        ).exists()
class GetArticle(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    comment_count: s.Field = s.IntegerField(default=0, read_only=True)
    article_type: s.Field = s.CharField()
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    # created_at: s.Field = s.DateTimeField(read_only=True)
    created_at: s.Field = s.SerializerMethodField()
    hospital: s.Field = s.SlugRelatedField(
        read_only=True,
        slug_field='name',
        # queryset=hm.Hospital.objects.all()
    )
    content: s.Field = s.CharField(read_only=False)
    article_attachment_assoc: s.Field = GetArticleAttachmentAssoc(many=True, read_only=True)
    attachment: cs.PutAttachment(read_only=True, many=True)
    article_keyword_assoc = ArticleKeywordAssoc(many=True, write_only=True, required=False)
    article_detail = ArticleDetailSer(many=False, write_only=True, required=False)
    article_auth = ArticleAuth(many=False, write_only=True, required=False)
    article_doctor_assoc = ArticleDoctorAssoc(many=True, write_only=True, required=False)
    is_like: s.Field = s.SerializerMethodField()

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, instance): ## 준호님의 요청으로 created_at을 XX분/시간/일/월/년 전으로 대체하는 로직 추후 작업시 MethodField를 DatatimeField로 변환 요망
        now = datetime.now().astimezone()
        created_at = instance.created_at
        total_seconds = (now-created_at).total_seconds()
        if total_seconds < 60:
            created_at = str(int(total_seconds))+ '초 전'
        elif total_seconds/60 < 60:
            created_at = str(int(total_seconds/60))+ '분 전'
        elif total_seconds/3600 < 24:
            created_at = str(int(total_seconds/3600))+ '시간 전'
        elif (total_seconds/3600)/24 < 30:
            created_at = str(int((total_seconds/3600)/24))+ '일 전'
        elif ((total_seconds/3600)/24)/30 < 12:
            created_at = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
        else:
            created_at = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return created_at

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_like(self, instance):
        if self.context['request'].user.is_anonymous:
            return False
        # if self.context['request'].user 
        return comm.ArticleLike.objects.filter(article=instance,
            user=self.context['request'].user
        ).exists()

class ArticleDetail(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user = CommunityUser(read_only=True)
    article_type: s.Field = s.CharField()
    up_count: s.Field = s.IntegerField(default=0, read_only=True)
    view_count: s.Field = s.IntegerField(default=0, read_only=True)
    # created_at: s.Field = s.DateTimeField(read_only=True)
    created_at: s.Field = s.SerializerMethodField()
    hospital: s.Field = s.SlugRelatedField(
        slug_field='name',
        queryset=hm.Hospital.objects.all()
    )
    content: s.Field = s.CharField(read_only=False)
    article_attachment_assoc: s.Field = GetArticleAttachmentAssoc(many=True, read_only=True)
    article_keyword_assoc = ArticleKeywordAssoc(many=True, write_only=True, required=False)
    article_detail = ArticleDetailSer(many=False, write_only=True, required=False)
    article_auth = ArticleAuth(many=False, write_only=True, required=False)
    article_doctor_assoc = ArticleDoctorAssoc(many=True, write_only=True, required=False)
    article_comment = ArticleComment(many=True, read_only=True)
    is_like: s.Field = s.SerializerMethodField()


    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id', 'status')

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_like(self, instance):
        return comm.ArticleLike.objects.filter(article=instance,
            user=self.context['request'].user
        ).exists()

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, instance): ## 준호님의 요청으로 created_at을 XX분/시간/일/월/년 전으로 대체하는 로직 추후 작업시 MethodField를 DatatimeField로 변환 요망
        now = datetime.now().astimezone()
        created_at = instance.created_at
        total_seconds = (now-created_at).total_seconds()
        if total_seconds < 60:
            created_at = str(int(total_seconds))+ '초 전'
        elif total_seconds/60 < 60:
            created_at = str(int(total_seconds/60))+ '분 전'
        elif total_seconds/3600 < 24:
            created_at = str(int(total_seconds/3600))+ '시간 전'
        elif (total_seconds/3600)/24 < 30:
            created_at = str(int((total_seconds/3600)/24))+ '일 전'
        elif ((total_seconds/3600)/24)/30 < 12:
            created_at = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
        else:
            created_at = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return created_at

class TreatmentKeyword(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    keyword: s.Field = s.CharField(read_only=True)

    class Meta:
        model = dosuri.community.models.TreatmentKeyword
        exclude = ('id', 'created_at', 'category')

class ArticleLike(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        write_only=True,
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    user = CommunityUser(read_only=True)
    is_like: s.Field = s.SerializerMethodField()
    created_at: s.Field = s.DateTimeField(read_only=True)
    class Meta:
        model = dosuri.community.models.ArticleLike
        exclude = ('id',)

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_like(self, instance):
        return comm.ArticleLike.objects.filter(article=instance.article,
            user=self.instance.user
        ).exists()

    def create(self, validated_data):
        try:
            exist_article_like = comm.ArticleLike.objects.get(**validated_data)
        except:
            exist_article_like = False
        if exist_article_like:
            exist_article_like.article.up_count = exist_article_like.article.up_count - 1
            exist_article_like.article.save()
            exist_article_like.delete()
            return exist_article_like
        article_like = comm.ArticleLike.objects.create(**validated_data)
        article_like.article.up_count = article_like.article.up_count + 1
        article_like.article.save()
        return article_like