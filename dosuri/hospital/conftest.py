import pytest
from dosuri.hospital import models as hm

@pytest.fixture
def address_서울시_강남구():
    return hm.Address.objects.create(
        do='서울시',
        gu='강남구'
    )


@pytest.fixture
def hospital_test_A(address_서울시_강남구):
    return hm.Hospital.objects.create(
        name='test_A',
        address=address_서울시_강남구
    )
