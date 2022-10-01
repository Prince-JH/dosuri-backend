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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_calendar')
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


class HospitalKeyword(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64)
    is_custom = models.BooleanField(default=False)  # 사용자가 추가한 키워드 True, 관리자가 추가한 키워드 False
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_keyword'


class HospitalKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    keyword = models.ForeignKey(HospitalKeyword, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_keyword_assoc'


class Doctor(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctor')
    thumbnail_url = models.CharField(max_length=512)
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    position = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor'


class DoctorDetail(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_detail')
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_detail'
