import pytest
from dosuri.hospital import (
    models as hm,
    constants as hc
)


@pytest.fixture
def address_서울시_강남구():
    return hm.Address.objects.create(
        do='서울시',
        gu='강남구'
    )


@pytest.fixture
def address_수원시_팔달구():
    return hm.Address.objects.create(
        do='수원시',
        gu='팔달구'
    )


@pytest.fixture
def hospital_test_A(address_서울시_강남구):
    return hm.Hospital.objects.create(
        name='test_A',
        address=address_서울시_강남구
    )

@pytest.fixture
def hospital_test_B(address_서울시_강남구):
    return hm.Hospital.objects.create(
        name='test_B',
        address=address_서울시_강남구
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
def hospital_url_1_test_A(hospital_test_A):
    return hm.HospitalImage.objects.create(
        hospital=hospital_test_A,
        url='url_1'
    )

@pytest.fixture
def hospital_url_2_test_A(hospital_test_A):
    return hm.HospitalImage.objects.create(
        hospital=hospital_test_A,
        url='url_2'
    )

@pytest.fixture
def hospital_url_3_test_B(hospital_test_B):
    return hm.HospitalImage.objects.create(
        hospital=hospital_test_B,
        url='url_3'
    )

@pytest.fixture
def hospital_url_4_test_B(hospital_test_B):
    return hm.HospitalImage.objects.create(
        hospital=hospital_test_B,
        url='url_4'
    )

@pytest.fixture
def doctor_A_hospital_A(hospital_test_A):
    return hm.Doctor.objects.create(
        hospital=hospital_test_A,
        name='test_A',
    )


@pytest.fixture
def description_A_doctor_A_test_A(doctor_A_hospital_A):
    return hm.DoctorDescription.objects.create(
        doctor=doctor_A_hospital_A,
        description='test_A',
    )

@pytest.fixture
def hospital_keyword_A():
    return hm.Keyword.objects.create(
        name='test_A',
        is_custom=False,
        domain=hc.KEYWORD_HOSPITAL
    )

@pytest.fixture
def hospital_A_keyword_A_assoc(hospital_test_A, hospital_keyword_A):
    return hm.HospitalKeywordAssoc.objects.create(
        hospital=hospital_test_A,
        keyword=hospital_keyword_A
    )

@pytest.fixture
def doctor_keyword_A():
    return hm.Keyword.objects.create(
        name='test_A',
        is_custom=False,
        domain=hc.KEYWORD_DOCTOR
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
        duration=30,
        description=None
    )
