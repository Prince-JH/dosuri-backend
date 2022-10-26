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