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
    def test_list_hospital_search_by_exist_name_should_return_one(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals/?search=test_A')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_search_by_not_exist_name_should_return_zero(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals/?search=test_B')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_create_hospital(self, client, address_서울시_강남구):
        data = {
            'address': address_서울시_강남구.uuid,
            'name': 'test hospital',
            'introduction': None,
            'phone_no': None,
            'is_partner': False,
            'opened_at': None
        }
        response = client.post('/hospital/v1/hospitals/', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1


class TestHospitalDetail:
    @pytest.mark.django_db
    def test_get_hospital_by_uuid(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals/{hospital_test_A.uuid}/')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['name'] == hospital_test_A.name


class TestHospitalCalendar:
    @pytest.mark.django_db
    def test_get_calendar_by_hospital(self, client, hospital_test_A, hospital_calendar_test_A):
        response = client.get(f'/hospital/v1/hospital-calendars/?hospital={hospital_test_A.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_get_calendars_at_once_by_hospitals(self, client, hospital_test_A, hospital_test_B,
                                                hospital_calendar_test_A, hospital_calendar_test_B):
        response = client.get(
            f'/hospital/v1/hospital-calendars/?hospital={hospital_test_A.uuid}&hospital={hospital_test_B.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 2


class TestHospitalImage:
    @pytest.mark.django_db
    def test_get_images_by_hospital_should_return_all_two_images(self, client, hospital_test_A, hospital_url_1_test_A,
                                                                 hospital_url_2_test_A):
        response = client.get(f'/hospital/v1/hospital-images/?hospital={hospital_test_A.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 2

    @pytest.mark.django_db
    def test_get_images_at_once_by_hospitals_should_return_all_four_images(self, client, hospital_test_A,
                                                                           hospital_test_B,
                                                                           hospital_url_1_test_A, hospital_url_2_test_A,
                                                                           hospital_url_3_test_B,
                                                                           hospital_url_4_test_B):
        response = client.get(
            f'/hospital/v1/hospital-images/?hospital={hospital_test_A.uuid}&hospital={hospital_test_B.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 4


class TestDoctor:
    @pytest.mark.django_db
    def test_list_doctor_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/doctors/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_doctor_should_return_one(self, client, doctor_A_test_A):
        response = client.get(f'/hospital/v1/doctors/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_doctor(self, client, hospital_test_A):
        data = {
            'hospital': hospital_test_A.uuid,
            'name': 'test doctor',
            'thumbnail_url': None,
            'title': 'chief',
            'position': 'therapist',
        }
        response = client.post('/hospital/v1/doctors/', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1


class TestDoctorDescription:
    @pytest.mark.django_db
    def test_list_doctor_description_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/doctor-descriptions/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_doctor_description_should_return_one(self, client, description_A_doctor_A_test_A):
        response = client.get(f'/hospital/v1/doctor-descriptions/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_doctor(self, client, doctor_A_test_A):
        data = {
            'doctor': doctor_A_test_A.uuid,
            'description': 'test description',
        }
        response = client.post('/hospital/v1/doctor-descriptions/', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1
