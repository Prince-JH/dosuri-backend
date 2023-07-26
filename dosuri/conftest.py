from datetime import datetime, timezone, timedelta

import pendulum
import pytest
from django.contrib.auth import get_user_model

from dosuri.common import models as cm
from dosuri.hospital import (
    models as hm,
    constants as hc
)
from dosuri.community import (
    models as cmm,
    constants as cmc
)
from dosuri.user.auth import get_tokens_for_user
from dosuri.user import models as um


@pytest.fixture
def user_dummy():
    return get_user_model().objects.create_user(
        username='dummy@dummy.com',
        nickname='dummy',
        birthday=datetime.now()
    )


@pytest.fixture
def user_dummy_1():
    return get_user_model().objects.create_user(
        username='dummy@dummy.net',
        nickname='dummy1'
    )


@pytest.fixture
def user_dummy_password():
    return get_user_model().objects.create_user(
        username='dummy@dummy.com',
        nickname='dummy',
        password='password'
    )


@pytest.fixture
def user_dummies():
    return [get_user_model().objects.create_user(
        username=f'dummy{i}@dummy.com',
        nickname=f'dummy{i}'
    ) for i in range(100)]


@pytest.fixture
def tokens_user_dummy(user_dummy):
    return get_tokens_for_user(user_dummy)


@pytest.fixture
def user_dummy_point_history_100(user_dummy):
    return um.UserPointHistory.objects.create_history(user_dummy, 100, 'test')


@pytest.fixture
def address_서울시_강남구():
    return cm.Address.objects.create(
        large_area='서울특별시',
        small_area='강남구'
    )


@pytest.fixture
def address_수원시_팔달구():
    return cm.Address.objects.create(
        large_area='경기도',
        small_area='수원시 팔달구'
    )


@pytest.fixture
def hospital_test_강남():
    return hm.Hospital.objects.create(
        name='test_A',
        latitude=37.517331925853,
        longitude=127.047377408384,
        opened_at=pendulum.datetime(2023, 1, 1),
        status=hc.HOSPITAL_ACTIVE
    )


@pytest.fixture
def hospital_test_수원():
    return hm.Hospital.objects.create(
        name='test_B',
        latitude=37.2826740965805,
        longitude=127.020135072307,
        opened_at=pendulum.datetime(2020, 1, 1),
        status=hc.HOSPITAL_ACTIVE
    )


@pytest.fixture
def hospital_test_C():
    return hm.Hospital.objects.create(
        name='test_C'
    )


@pytest.fixture
def hospital_lat100_long100():
    return hm.Hospital.objects.create(
        name='test_D',
        latitude=100,
        longitude=100
    )


@pytest.fixture
def hospital_calendar_test_A(hospital_test_강남):
    return hm.HospitalCalendar.objects.create(
        hospital=hospital_test_강남,
        monday='10:00 ~ 20:00',
        tuesday='10:00 ~ 20:00',
        wednesday='10:00 ~ 20:00',
        thursday='10:00 ~ 20:00',
        friday='10:00 ~ 20:00',
        saturday='10:00 ~ 20:00',
        sunday='',
    )


@pytest.fixture
def hospital_calendar_test_B(hospital_test_수원):
    return hm.HospitalCalendar.objects.create(
        hospital=hospital_test_수원,
        monday='10:00 ~ 20:00',
        tuesday='10:00 ~ 20:00',
        wednesday='10:00 ~ 20:00',
        thursday='10:00 ~ 20:00',
        friday='10:00 ~ 20:00',
        saturday='10:00 ~ 20:00',
        sunday='',
    )


@pytest.fixture
def user_dummy_address_서울(user_dummy):
    return um.UserAddress.objects.create_etc_address(
        user=user_dummy,
        name='서울',
        address='서울특별시 강남구 강남구청',
        latitude=37.517331925853,
        longitude=127.047377408384
    )


@pytest.fixture
def user_dummy_address_서울_main(user_dummy_address_서울):
    um.UserAddress.objects.set_main_address(user_dummy_address_서울)
    return user_dummy_address_서울


@pytest.fixture
def doctor_A_hospital_A(hospital_test_강남):
    return hm.Doctor.objects.create(
        hospital=hospital_test_강남,
        name='test_A',
        position=hc.POSITION_DOCTOR
    )


@pytest.fixture
def therapist_A_hospital_A(hospital_test_강남):
    return hm.Doctor.objects.create(
        hospital=hospital_test_강남,
        name='test_A',
        position=hc.POSITION_THERAPIST
    )


@pytest.fixture
def description_A_doctor_A_test_A(doctor_A_hospital_A):
    return hm.DoctorDescription.objects.create(
        doctor=doctor_A_hospital_A,
        description='test_A',
    )


@pytest.fixture
def hospital_keyword_A():
    return hm.HospitalKeyword.objects.create(
        name='test_A',
        is_custom=False
    )


@pytest.fixture
def hospital_keyword_B():
    return hm.HospitalKeyword.objects.create(
        name='test_B',
        is_custom=False
    )


@pytest.fixture
def hospital_A_keyword_A_assoc(hospital_test_강남, hospital_keyword_A):
    return hm.HospitalKeywordAssoc.objects.create(
        hospital=hospital_test_강남,
        keyword=hospital_keyword_A
    )


@pytest.fixture
def hospital_B_keyword_B_assoc(hospital_test_수원, hospital_keyword_B):
    return hm.HospitalKeywordAssoc.objects.create(
        hospital=hospital_test_수원,
        keyword=hospital_keyword_B
    )


@pytest.fixture
def doctor_keyword_A():
    return hm.DoctorKeyword.objects.create(
        name='test_A',
        is_custom=False
    )


@pytest.fixture
def doctor_A_keyword_A_assoc(doctor_A_hospital_A, doctor_keyword_A):
    return hm.DoctorKeywordAssoc.objects.create(
        doctor=doctor_A_hospital_A,
        keyword=doctor_keyword_A
    )


@pytest.fixture
def hospital_treatments_test_A(hospital_test_강남):
    return hm.HospitalTreatment.objects.create(
        name='treatment_A',
        hospital=hospital_test_강남,
        price=80000,
        price_per_hour=160000,
        description=None
    )


@pytest.fixture
def hospital_treatments_A_hospital_B(hospital_test_수원):
    return hm.HospitalTreatment.objects.create(
        name='treatment_A',
        hospital=hospital_test_수원,
        price=80000,
        price_per_hour=160000,
        description=None
    )


@pytest.fixture
def article_A_hospital_A(hospital_test_강남, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_강남,
        content='A',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def treatment_category_A():
    return cmm.TreatmentCategory.objects.create(
        category="도수 치료"
    )


@pytest.fixture
def article_keyword_A(treatment_category_A):
    return cmm.TreatmentKeyword.objects.create(
        keyword="도수 치료",
        category=treatment_category_A,
    )


@pytest.fixture
def attachment_A():
    return cm.Attachment.objects.create(
        bucket_name="test_bucket_A",
        path="test_path_A"
    )


@pytest.fixture
def attachment_B():
    return cm.Attachment.objects.create(
        bucket_name="test_bucket_A",
        path="test_path_B"
    )


@pytest.fixture
def article_B_hospital_A(hospital_test_강남, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_강남,
        content='B',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def article_A_hospital_B(hospital_test_수원, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_수원,
        content='A',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def article_A_hospital_C(hospital_test_C, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_C,
        content='A',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def article_question(user_dummy):
    return cmm.Article.objects.create(
        content='A',
        user=user_dummy,
        article_type=cmc.ARTICLE_QUESTION
    )


@pytest.fixture
def article_auth_A_article_A_hospital_B(article_A_hospital_B, user_dummy):
    return cmm.ArticleAuth.objects.create(
        article=article_A_hospital_B,
        status=cmc.STATUS_INCOMPLETE
    )


@pytest.fixture
def hospital_search_A_user_dummy(user_dummy):
    return hm.HospitalSearch.objects.create(
        user=user_dummy,
        word='A'
    )


@pytest.fixture
def hospital_search_B_user_dummy(user_dummy):
    return hm.HospitalSearch.objects.create(
        user=user_dummy,
        word='B'
    )


@pytest.fixture
def insurance_A():
    return um.Insurance.objects.create(
        name='A'
    )


@pytest.fixture
def insurance_user_assoc_old(insurance_A, user_dummy):
    assoc = um.InsuranceUserAssoc.objects.create(
        insurance=insurance_A,
        user=user_dummy
    )
    assoc.created_at = datetime(2021, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
    assoc.save()
    return assoc


@pytest.fixture
def insurance_user_assoc_new(insurance_A, user_dummy):
    return um.InsuranceUserAssoc.objects.create(
        insurance=insurance_A,
        user=user_dummy,
        created_at=datetime(2021, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def user_dummy_address_home(user_dummy):
    return um.UserAddress.objects.create_home_address(user_dummy, 'home', '수원시 팔달구 아주로 17', 123.123, 123.123)


@pytest.fixture
def user_dummy_address_office(user_dummy):
    return um.UserAddress.objects.create_office_address(user_dummy, 'office', '서초대로 343 신덕빌딩', 123.123, 123.123)


@pytest.fixture
def user_dummy_address_etc(user_dummy):
    return um.UserAddress.objects.create_etc_address(user_dummy, 'home', '강남구 삼성동 106', 123.123, 123.123)


@pytest.fixture
def user_setting(user_dummy):
    return um.UserSetting.objects.create(
        user=user_dummy,
        agree_marketing_personal_info=True,
        agree_general_push=True,
        agree_marketing_push=True,
        agree_marketing_email=True,
        agree_marketing_sms=True
    )


@pytest.fixture
def hospital_test_강남_contact_counseling(hospital_test_강남):
    return hm.HospitalContactPoint.objects.create(
        hospital=hospital_test_강남,
        contact_type=hc.CONTACT_TYPE_COUNSEL,
        contact_point='01012345678'
    )
