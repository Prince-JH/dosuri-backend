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
        nickname='dummy'
    )


@pytest.fixture
def tokens_user_dummy(user_dummy):
    return get_tokens_for_user(user_dummy)


@pytest.fixture
def user_dummy_point_history_100(user_dummy):
    return um.UserPointHistory.objects.create_history(user_dummy, 100, 'test')


@pytest.fixture
def address_서울시_강남구():
    return cm.Address.objects.create(
        large_area='서울',
        small_area='강남구'
    )


@pytest.fixture
def address_수원시_팔달구():
    return cm.Address.objects.create(
        large_area='경기',
        small_area='수원시 팔달구'
    )


@pytest.fixture
def hospital_test_A():
    return hm.Hospital.objects.create(
        name='test_A'
    )


@pytest.fixture
def hospital_test_B():
    return hm.Hospital.objects.create(
        name='test_B'
    )


@pytest.fixture
def hospital_test_C():
    return hm.Hospital.objects.create(
        name='test_C'
    )


@pytest.fixture
def hospital_calendar_test_A(hospital_test_A):
    return hm.HospitalCalendar.objects.create(
        hospital=hospital_test_A,
        monday='10:00 ~ 20:00',
        tuesday='10:00 ~ 20:00',
        wednesday='10:00 ~ 20:00',
        thursday='10:00 ~ 20:00',
        friday='10:00 ~ 20:00',
        saturday='10:00 ~ 20:00',
        sunday='',
    )


@pytest.fixture
def hospital_calendar_test_B(hospital_test_B):
    return hm.HospitalCalendar.objects.create(
        hospital=hospital_test_B,
        monday='10:00 ~ 20:00',
        tuesday='10:00 ~ 20:00',
        wednesday='10:00 ~ 20:00',
        thursday='10:00 ~ 20:00',
        friday='10:00 ~ 20:00',
        saturday='10:00 ~ 20:00',
        sunday='',
    )


@pytest.fixture
def assoc_hospital_A_address_강남(hospital_test_A, address_서울시_강남구):
    return hm.HospitalAddressAssoc.objects.create(
        hospital=hospital_test_A,
        address=address_서울시_강남구
    )


@pytest.fixture
def assoc_hospital_B_address_수원(hospital_test_B, address_수원시_팔달구):
    return hm.HospitalAddressAssoc.objects.create(
        hospital=hospital_test_B,
        address=address_수원시_팔달구
    )


@pytest.fixture
def assoc_address_수원_user_dummy(address_수원시_팔달구, user_dummy):
    return um.AddressUserAssoc.objects.create(
        address=address_수원시_팔달구,
        user=user_dummy
    )


@pytest.fixture
def doctor_A_hospital_A(hospital_test_A):
    return hm.Doctor.objects.create(
        hospital=hospital_test_A,
        name='test_A',
        position=hc.POSITION_DOCTOR
    )


@pytest.fixture
def therapist_A_hospital_A(hospital_test_A):
    return hm.Doctor.objects.create(
        hospital=hospital_test_A,
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
def hospital_A_keyword_A_assoc(hospital_test_A, hospital_keyword_A):
    return hm.HospitalKeywordAssoc.objects.create(
        hospital=hospital_test_A,
        keyword=hospital_keyword_A
    )


@pytest.fixture
def hospital_B_keyword_B_assoc(hospital_test_B, hospital_keyword_B):
    return hm.HospitalKeywordAssoc.objects.create(
        hospital=hospital_test_B,
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
def hospital_treatments_test_A(hospital_test_A):
    return hm.HospitalTreatment.objects.create(
        name='treatment_A',
        hospital=hospital_test_A,
        price=80000,
        price_per_hour=160000,
        description=None
    )


@pytest.fixture
def article_A_hospital_A(hospital_test_A, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_A,
        content='A',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def article_B_hospital_A(hospital_test_A, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_A,
        content='B',
        user=user_dummy,
        article_type=cmc.ARTICLE_REVIEW
    )


@pytest.fixture
def article_A_hospital_B(hospital_test_B, user_dummy):
    return cmm.Article.objects.create(
        hospital=hospital_test_B,
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
def attachment_A():
    return cm.Attachment.objects.create(
        bucket_name='test bucket',
        path='test path'
    )
