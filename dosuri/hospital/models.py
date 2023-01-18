from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models, transaction

from dosuri.common import models as cm
from dosuri.user import models as um
from dosuri.hospital import model_managers as hmm


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
    view_count = models.IntegerField(default=0)
    is_partner = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = hmm.HospitalManager()

    class Meta:
        db_table = 'hospital'
        ordering = ['-id']

    def increase_view_count(self):
        with transaction.atomic():
            self.view_count += 1
            self.save()


class HospitalAttachmentAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_attachment_assoc')
    attachment = models.ForeignKey(cm.Attachment, on_delete=models.CASCADE, related_name='hospital_attachment_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_attachment_assoc'
        ordering = ['-id']


class HospitalCalendar(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name='hospital_calendar')
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


class HospitalKeyword(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64)
    is_custom = models.BooleanField(default=False)  # 사용자가 추가한 키워드 True, 관리자가 추가한 키워드 False
    created_at = models.DateTimeField(auto_now_add=True)

    objects = hmm.HospitalKeywordManager()

    class Meta:
        db_table = 'hospital_keyword'
        ordering = ['-id']


class HospitalKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    keyword = models.ForeignKey(HospitalKeyword, on_delete=models.CASCADE, related_name='hospital_keyword_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hospital_keyword_assoc'
        ordering = ['-id']


class Doctor(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=64)
    position = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor'
        ordering = ['-id']


class DoctorAttachmentAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_attachment_assoc')
    attachment = models.ForeignKey(cm.Attachment, on_delete=models.CASCADE, related_name='doctor_attachment_assoc')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_attachment_assoc'
        ordering = ['-id']


class DoctorDescription(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_detail')
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_detail'
        ordering = ['-id']


class DoctorKeyword(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    name = models.CharField(max_length=64)
    is_custom = models.BooleanField(default=False)  # 사용자가 추가한 키워드 True, 관리자가 추가한 키워드 False
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor_keyword'
        ordering = ['-id']


class DoctorKeywordAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
    keyword = models.ForeignKey(DoctorKeyword, on_delete=models.CASCADE, related_name='doctor_keyword_assoc')
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


class HospitalUserAssoc(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_user_assoc')
    user = models.ForeignKey(um.User, on_delete=models.CASCADE, related_name='hospital_user_assoc')
    is_up = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = hmm.HospitalUserAssocManager()

    class Meta:
        db_table = 'hospital_user_assoc'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'user'], name='hospital_user_unique_constraint'),
        ]


class HospitalSearch(models.Model):
    uuid = models.CharField(max_length=32, default=generate_uuid, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='hospital_search')
    word = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = hmm.HospitalSearchManager()

    class Meta:
        db_table = 'hospital_search'
        ordering = ['-id']
