from uuid import uuid4

from django.db import models

from dosuri.common import models as cm


def generate_uuid():
    return uuid4().hex


class Hospital(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    code = models.CharField(max_length=128, null=True)
    address = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, null=True)
    area = models.CharField(max_length=32, null=True)
    phone_no = models.CharField(max_length=32, null=True)
    up_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_partner = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital'
        ordering = ['-id']


class HospitalImage(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    title = models.CharField(max_length=64, default='')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_image')
    url = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_image'
        ordering = ['-id']


class HospitalCalendar(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_calendar')
    monday = models.CharField(max_length=128, null=True)
    tuesday = models.CharField(max_length=128, null=True)
    wednesday = models.CharField(max_length=128, null=True)
    thursday = models.CharField(max_length=128, null=True)
    friday = models.CharField(max_length=128, null=True)
    saturday = models.CharField(max_length=128, null=True)
    sunday = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_calendar'
        ordering = ['-id']


class HospitalAddressAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_address_assoc')
    address = models.ForeignKey(cm.Address, on_delete=models.CASCADE, related_name='hospital_address_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_address_assoc'
        ordering = ['-id']


class Keyword(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64)
    is_custom = models.BooleanField(default=False)  # 사용자가 추가한 키워드 True, 관리자가 추가한 키워드 False
    domain = models.CharField(max_length=64)  # doctor keyword / hospital keyword
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_keyword'
        ordering = ['-id']


class HospitalKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_keyword_assoc'
        ordering = ['-id']


class Doctor(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctor')
    thumbnail_url = models.CharField(max_length=512, null=True)
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    position = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor'
        ordering = ['-id']


class DoctorDescription(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_detail')
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_detail'
        ordering = ['-id']


class DoctorKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_keyword_assoc'
        ordering = ['-id']


class HospitalTreatment(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=128, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_treatment')
    price = models.IntegerField()
    price_per_hour = models.IntegerField(null=True)
    description = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_treatment'
        ordering = ['-id']

# class Review(models.Model):
#     uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
#     hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
#     keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'review'
