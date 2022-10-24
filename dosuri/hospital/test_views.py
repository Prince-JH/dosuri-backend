import json

import pytest

from dosuri.hospital import models as hm


class TestHospitalList:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/hospital/v1/hospitals/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, hospital_test_A):
        response = client.get('/hospital/v1/hospitals/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_filter_with_address(self, client, hospital_test_A, address_서울시_강남구, address_수원시_팔달구):
        response = client.get(f'/hospital/v1/hospitals/?address={address_서울시_강남구.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_hospital(self, client, address_서울시_강남구):
        data = {
            'address': address_서울시_강남구.uuid,
            'name': 'test hospital',
            'introduction': '',
            'phone_no': '',
            'is_partner': False,
            'opened_at': None
        }
        response = client.post('/hospital/v1/hospitals/', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1


class TestHospitalView:
    @pytest.mark.django_db
    def test_get_hospital_by_uuid(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals/{hospital_test_A.uuid}/')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['name'] == hospital_test_A.name
