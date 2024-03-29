from uuid import uuid4

from django.db import models
from dosuri.user.models import User, UserPointHistory
from dosuri.hospital.models import Hospital, Doctor, HospitalTreatment
from dosuri.community import constants as cmc
from dosuri.common.models import Attachment


def generate_uuid():
    return uuid4().hex


class TreatmentCategory(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    category = models.CharField(max_length=15, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'treatment_category'
        ordering = ['-id']


class TreatmentKeyword(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    keyword = models.CharField(max_length=15, null=False)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE, related_name='treatmeny_keyword',
                                 null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'treatment_keyword'
        ordering = ['id']


class Article(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    status = models.CharField(max_length=15, default=cmc.STATUS_INCOMPLETE)
    article_type = models.CharField(default=None, null=True, max_length=20)
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='article', null=True)
    content = models.CharField(max_length=1200, blank=True, null=False, default='')  ## 후기 최대글자 한글은 3 bytes (최대 400글자)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article'
        ordering = ['-id']

    def authenticate_article(self):
        if self.article_type == cmc.ARTICLE_QUESTION:
            return
        if self.status == cmc.STATUS_COMPLETE:
            return
        user = self.user
        auth = self.article_auth
        auth.status = cmc.STATUS_COMPLETE
        auth.save()
        UserPointHistory.objects.give_point(user, 1000, '후기 인증')


class ArticleAttachmentAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_attachment_assoc')
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, related_name='article_attachment_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_attachment_assoc'
        ordering = ['-id']


# class ArticleMeta(models.Model):
#     uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
#     article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_meta')
#     hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='article_meta')
#     cost = models.IntegerField(default=None, null=True)
#     treat_count = models.IntegerField(default=None, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'article_meta'
#         ordering = ['-id']

class ArticleDetail(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='article_detail')
    treatment_effect = models.IntegerField(default=None, null=True)
    doctor_kindness = models.IntegerField(default=None, null=True)
    therapist_kindness = models.IntegerField(default=None, null=True)
    staff_kindness = models.IntegerField(default=None, null=True)
    clean_score = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.IntegerField(default=None, null=True)
    treat_count = models.IntegerField(default=None, null=True)

    class Meta:
        db_table = 'article_detail'
        ordering = ['-id']


class ArticleAuth(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='article_auth')
    sensitive_agreement = models.BooleanField(default=False)
    personal_agreement = models.BooleanField(default=False)
    status = models.CharField(max_length=15, default=cmc.STATUS_INCOMPLETE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_auth'
        ordering = ['-id']

    def __str__(self):
        return self.status


class AuthAttachmentAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_auth = models.ForeignKey(ArticleAuth, on_delete=models.CASCADE, related_name='auth_attachment_assoc')
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, related_name='auth_attachment_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_attachment_assoc'
        ordering = ['-id']


class ArticleDoctorAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_doctor_assoc')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='article_doctor_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_doctor_assoc'
        ordering = ['-id']


# class HospitalAssoc(models.Model):
#     uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='hospital_assoc')
#     hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_assoc')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'hospital_assoc'
#         ordering = ['-id']

class ArticleKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='treatment_keyword_assoc')
    treatment_keyword = models.ForeignKey(TreatmentKeyword, on_delete=models.CASCADE,
                                          related_name='treatment_keyword_assoc', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_keyword_assoc'
        ordering = ['-id']


class ArticleLike(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_like')
    is_like = models.BooleanField(default=True)  #### 추후 있을 싫어요 기능을 위한 bool field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_like'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='One like by article')
        ]


class ArticleComment(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment')
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1200)  ## 댓글 최대글자 한글은 3 bytes (최대 400글자)

    class Meta:
        db_table = 'article_comment'
        ordering = ['created_at']
        # ordering = ['-id']


class ArticleThread(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_thread')
    article_comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='article_thread')
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1200)  ## 댓글 최대글자 한글은 3 bytes (최대 400글자)
    mention_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_thread_mention_user',
                                     null=False)

    class Meta:
        db_table = 'article_thread'
        ordering = ['created_at']
