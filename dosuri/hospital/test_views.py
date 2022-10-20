import json

import pytest

from dosuri.hospital import models as hm


class TestHospitalList:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/api/hospital/v1/hospitals/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, hospital_test_A):
        response = client.get('/api/hospital/v1/hospitals/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, address_서울시_강남구):
        data = {
            'address': address_서울시_강남구.uuid,
            'name': 'test hospital',
            'introduction': '',
            'phone_no': '',
            'is_partner': False,
            'opened_at': None
        }
        response = client.post('/api/hospital/v1/hospitals/', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1
