from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from dosuri.user import model_managers as umm


def generate_uuid():
    return uuid4().hex


class User(AbstractUser):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    nickname = models.CharField(max_length=32, unique=True, null=True)
    address_id = models.CharField(max_length=16, default='', blank=True)
    birthday = models.DateTimeField(null=True)
    sex = models.CharField(max_length=16, default='', blank=True)
    is_real = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = umm.DosuriUserManager()

    class Meta:
        db_table = 'user'
        app_label = 'dosuri'


class InsuranceLog(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user_id = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'insurance_log'
        ordering = ['-id']
