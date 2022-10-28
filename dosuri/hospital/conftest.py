import pytest
from dosuri.hospital import models as hm


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
def doctor_A_test_A(hospital_test_A):
    return hm.Doctor.objects.create(
        hospital=hospital_test_A,
        name='test_A',
    )


@pytest.fixture
def description_A_doctor_A_test_A(doctor_A_test_A):
    return hm.DoctorDescription.objects.create(
        doctor=doctor_A_test_A,
        description='test_A',
    )