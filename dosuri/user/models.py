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
    sex = models.CharField(max_length=32, null=True)
    name = models.CharField(max_length=64, null=True)
    phone_no = models.CharField(max_length=32, null=True)
    is_real = models.BooleanField(default=True)
    unread_notice = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = umm.DosuriUserManager()

    class Meta:
        db_table = 'user'
        app_label = 'dosuri'
        ordering = ['-id']

    def is_new(self):
        qs = UserAddress.objects.filter(user=self)
        return False if qs.exists() else True

    def resign(self):
        self.delete()


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

    objects = umm.AddressUserAssocManager()

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


class UserPointHistory(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_point_history')
    modify_point = models.IntegerField(default=0)
    total_point = models.IntegerField(default=0)
    content = models.CharField(max_length=128, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = umm.UserPointHistoryManager()

    class Meta:
        db_table = 'user_point_history'
        ordering = ['-id']


class UserNotification(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_notification')
    content = models.CharField(max_length=128, default='')
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = umm.UserNotificationManager()

    class Meta:
        db_table = 'user_notification'
        ordering = ['-id']


class UserResignHistory(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    username = models.CharField(max_length=150)
    reason = models.CharField(max_length=256, default='')

    class Meta:
        db_table = 'user_resign_history'
        ordering = ['-id']


class UserAddress(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_address')
    name = models.CharField(max_length=32, null=True)
    address = models.CharField(max_length=64)
    address_type = models.CharField(max_length=64)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(default=0)  # 위도, y_pos
    longitude = models.FloatField(default=0)  # 경도, x_pos

    objects = umm.UserAddressManager()


class UserPersonalInformationAgreement(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_personal_information_agreement')
    agree_push = models.BooleanField(default=True)
    agree_email = models.BooleanField(default=True)
    agree_sms = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
