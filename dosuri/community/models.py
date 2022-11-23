from uuid import uuid4

from django.db import models


def generate_uuid():
    return uuid4().hex

class Article(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ArticleMeta(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital')
    cost = models.IntegerField(default=None, null=True)
    treat_count = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_meta'
        ordering = ['-id']

class ArticleDetail(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    treatment_effect = models.IntegerField(default=None, null=True)
    doctor_kindness = models.IntegerField(default=None, null=True)
    therapist_kindness = models.IntegerField(default=None, null=True)
    clean_score = models.IntegerField(default=None, null=True)
    content = models.CharField(max_length=1200) ## 후기 최대글자 한글은 3 bytes (최대 400글자)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_detail'
        ordering = ['-id']

class ArticleAuth(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    sensitive_agreement = models.BooleanField(default=False)
    personal_agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_auth'
        ordering = ['-id']

class AuthAttach(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_auth_id = models.ForeignKey(ArticleAuth, on_delete=models.CASCADE, related_name='article_auth')
    path = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_attach'
        ordering = ['-id']

class ArticleAttach(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    path = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_attach'
        ordering = ['-id']

class DoctorAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_meta_id = models.ForeignKey(ArticleMeta, on_delete=models.CASCADE, related_name='article_meta')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_assoc'
        ordering = ['-id']

class HospitalAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    article_meta_id = models.ForeignKey(ArticleMeta, on_delete=models.CASCADE, related_name='article_meta')
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_assoc'
        ordering = ['-id']

class ArticleComment(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1200) ## 댓글 최대글자 한글은 3 bytes (최대 400글자)

    class Meta:
        db_table = 'article_comment'
        ordering = ['-id']

class ArticleThread(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    article_comment_id = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='article_comment')
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1200) ## 댓글 최대글자 한글은 3 bytes (최대 400글자)

    class Meta:
        db_table = 'article_thread'
        ordering = ['-id']
