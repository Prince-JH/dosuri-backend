from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from dosuri.user import model_managers as umm
from dosuri.common import models as cm


def generate_uuid():
    return uuid4().hex


class User(AbstractUser):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    nickname = models.CharField(max_length=32, unique=True, null=True)
    birthday = models.DateTimeField(null=True)
    sex = models.CharField(max_length=16, default='', blank=True)
    phone_no = models.CharField(max_length=32, default='', blank=True)
    is_real = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = umm.DosuriUserManager()

    class Meta:
        db_table = 'user'
        app_label = 'dosuri'
        ordering = ['-id']


class Insurance(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'insurance'
        ordering = ['-id']


class InsuranceUserAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='insurance_user_assoc')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='insurance_user_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'insurance_user_assoc'
        ordering = ['-id']


class PainArea(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pain_area'
        ordering = ['-id']


class AddressUserAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    address = models.ForeignKey(cm.Address, on_delete=models.CASCADE, related_name='address_user_assoc')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='address_user_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'address_user_assoc'
        ordering = ['-id']


class PainAreaUserAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    pain_area = models.ForeignKey(PainArea, on_delete=models.CASCADE, related_name='pain_area_user_assoc')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='pain_area_user_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pain_area_user_assoc'
        ordering = ['-id']
