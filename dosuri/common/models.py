from uuid import uuid4
from django.db import models

from dosuri.common import model_managers as cmm


def generate_uuid():
    return uuid4().hex


class Address(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    do = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    gun = models.CharField(max_length=32, null=True)
    gu = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = cmm.AddressManager()

    class Meta:
        db_table = 'address'
        ordering = ['-id']

