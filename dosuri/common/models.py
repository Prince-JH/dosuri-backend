from uuid import uuid4
from django.db import models

from dosuri.common import model_managers as cmm


def generate_uuid():
    return uuid4().hex


class Address(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    large_area = models.CharField(max_length=32, null=True)  # 도명/특별시명
    small_area = models.CharField(max_length=32, null=True)  # 시/군/구
    created_at = models.DateTimeField(auto_now_add=True)

    objects = cmm.AddressManager()

    class Meta:
        db_table = 'address'
        ordering = ['-id']
