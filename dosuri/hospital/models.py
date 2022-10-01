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

    class Meta:
        db_table = 'address'


class Hospital(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='hospital')
    name = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, default='', blank=True)
    phone_no = models.CharField(max_length=32, default='', blank=True)
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_partner = models.BooleanField(default=False)
    opened_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital'


class HospitalImage(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_image')
    url = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_image'


class HospitalCalendar(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_image')
    monday = models.CharField(max_length=128, default='', blank=True)
    tuesday = models.CharField(max_length=128, default='', blank=True)
    wednesday = models.CharField(max_length=128, default='', blank=True)
    thursday = models.CharField(max_length=128, default='', blank=True)
    friday = models.CharField(max_length=128, default='', blank=True)
    saturday = models.CharField(max_length=128, default='', blank=True)
    sunday = models.CharField(max_length=128, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_calendar'
