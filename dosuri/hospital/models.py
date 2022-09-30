from uuid import uuid4

from django.db import models


def generate_uuid():
    return uuid4().hex


class Address(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    do = models.CharField(max_length=32, default='', blank=True)
    city = models.CharField(max_length=32, default='', blank=True)
    gun = models.CharField(max_length=32, default='', blank=True)
    gu = models.CharField(max_length=32, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Hospital(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, default='', blank=True)
    phone_no = models.CharField(max_length=32, default='', blank=True)
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_partner = models.BooleanField(default=False)
    opened_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
