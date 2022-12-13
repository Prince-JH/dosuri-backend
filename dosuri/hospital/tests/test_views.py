import json

import pytest

from dosuri.hospital import (
    models as hm,
    constants as hc
)


class TestHospitalList:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/hospital/v1/hospitals')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, hospital_test_A):
        response = client.get('/hospital/v1/hospitals')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_filter_with_address(self, client, hospital_test_A, address_서울시_강남구, address_수원시_팔달구):
        response = client.get(f'/hospital/v1/hospitals?hospital_address_assoc_address={address_서울시_강남구.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_search_by_exist_name_should_return_one(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals?search=test_A')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_search_by_not_exist_name_should_return_zero(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals?search=test_B')
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
            'opened_at': None,
            'area': None
        }
        response = client.post('/hospital/v1/hospitals', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1

    @pytest.mark.django_db
    def test_hospital_list_order_by_review_count(
            self, client, hospital_test_A, hospital_test_B, hospital_test_C, article_A_hospital_A, article_B_hospital_A,
            article_A_hospital_B):
        response = client.get('/hospital/v1/hospitals?ordering=-article_count', content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert content['results'][0]['uuid'] == hospital_test_A.uuid
        assert content['results'][1]['uuid'] == hospital_test_B.uuid
        assert content['results'][2]['uuid'] == hospital_test_C.uuid

    @pytest.mark.django_db
    def test_hospital_list_order_by_review_new(
            self, client, hospital_test_A, hospital_test_B, hospital_test_C, article_A_hospital_A, article_B_hospital_A,
            article_A_hospital_B):
        response = client.get('/hospital/v1/hospitals?ordering=-latest_article_created_at',
                              content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert content['results'][0]['uuid'] == hospital_test_B.uuid
        assert content['results'][1]['uuid'] == hospital_test_A.uuid
        assert content['results'][2]['uuid'] == hospital_test_C.uuid


class TestHospitalDetail:
    @pytest.mark.django_db
    def test_get_hospital_by_uuid(self, client, hospital_test_A):
        response = client.get(f'/hospital/v1/hospitals/{hospital_test_A.uuid}')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['name'] == hospital_test_A.name


class TestHospitalCalendar:
    @pytest.mark.django_db
    def test_get_calendar_by_hospital(self, client, hospital_test_A, hospital_calendar_test_A):
        response = client.get(f'/hospital/v1/hospital-calendars?hospital={hospital_test_A.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_get_calendars_at_once_by_hospitals(self, client, hospital_test_A, hospital_test_B,
                                                hospital_calendar_test_A, hospital_calendar_test_B):
        response = client.get(
            f'/hospital/v1/hospital-calendars?hospital={hospital_test_A.uuid}&hospital={hospital_test_B.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 2


class TestHospitalImage:
    @pytest.mark.django_db
    def test_get_images_by_hospital_should_return_all_two_images(self, client, hospital_test_A, hospital_image_1_test_A,
                                                                 hospital_image_2_test_A):
        response = client.get(f'/hospital/v1/hospital-images?hospital={hospital_test_A.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 2

    @pytest.mark.django_db
    def test_get_images_at_once_by_hospitals_should_return_all_four_images(self, client, hospital_test_A,
                                                                           hospital_test_B,
                                                                           hospital_image_1_test_A,
                                                                           hospital_image_2_test_A,
                                                                           hospital_image_3_test_B,
                                                                           hospital_image_4_test_B):
        response = client.get(
            f'/hospital/v1/hospital-images?hospital={hospital_test_A.uuid}&hospital={hospital_test_B.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 4

    # @pytest.mark.django_db
    # def test_get_images_at_once_by_hospitals_in_body_should_return_all_four_images(
    #         self, client, hospital_test_A, hospital_test_B, hospital_test_C, hospital_image_1_test_A,
    #         hospital_image_2_test_A, hospital_image_3_test_B, hospital_image_4_test_B, hospital_image_5_test_C):
    #     data = {
    #         'hospitals': [hospital_test_A.uuid, hospital_test_B.uuid]
    #     }
    #     response = client.get('/hospital/v1/hospital-images', data=data, content_type='application/json')
    #     content = json.loads(response.content)
    #
    #     assert response.status_code == 200
    #     assert len(content) == 4


class TestHospitalAddressAssoc:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/hospital/v1/hospital-address-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, assoc_hospital_A_address_강남):
        response = client.get('/hospital/v1/hospital-address-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1


class TestDoctor:
    @pytest.mark.django_db
    def test_list_doctor_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/doctors')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_doctor_should_return_one(self, client, doctor_A_hospital_A):
        response = client.get(f'/hospital/v1/doctors')
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
            'subtitle': 'chief',
            'position': 'therapist',
        }
        response = client.post('/hospital/v1/doctors', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1


class TestDoctorDescription:
    @pytest.mark.django_db
    def test_list_doctor_description_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/doctor-descriptions')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_doctor_description_should_return_one(self, client, description_A_doctor_A_test_A):
        response = client.get(f'/hospital/v1/doctor-descriptions')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_doctor_description(self, client, doctor_A_hospital_A):
        data = {
            'doctor': doctor_A_hospital_A.uuid,
            'description': 'test description',
        }
        response = client.post('/hospital/v1/doctor-descriptions', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Hospital.objects.all().count() == 1


class TestKeyword:
    @pytest.mark.django_db
    def test_list_keyword_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/keywords')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 0

    @pytest.mark.django_db
    def test_list_hospital_keyword_should_return_one(self, client, hospital_keyword_A):
        response = client.get(f'/hospital/v1/keywords')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 1

    @pytest.mark.django_db
    def test_create_keyword(self, client):
        data = {
            'name': 'test',
            'is_custom': False,
            'domain': hc.KEYWORD_HOSPITAL
        }
        response = client.post('/hospital/v1/keywords', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.Keyword.objects.all().count() == 1

    @pytest.mark.django_db
    def test_list_hospital_keyword_should_return_one(self, client, hospital_A_keyword_A_assoc, hospital_test_A):
        response = client.get(f'/hospital/v1/keywords?hospital_keyword_assoc__hospital={hospital_test_A.uuid}',
                              content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 1


class TestHospitalKeywordAssoc:
    @pytest.mark.django_db
    def test_list_hospital_keyword_assoc_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/hospital-keyword-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_keyword_assoc_should_return_one(self, client, hospital_A_keyword_A_assoc):
        response = client.get(f'/hospital/v1/hospital-keyword-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_hospital_keyword_assoc(self, client, hospital_test_A, hospital_keyword_A):
        data = {
            'hospital': hospital_test_A.uuid,
            'keyword': hospital_keyword_A.uuid
        }
        response = client.post('/hospital/v1/hospital-keyword-assocs', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.HospitalKeywordAssoc.objects.all().count() == 1


class TestDoctorKeywordAssoc:
    @pytest.mark.django_db
    def test_list_doctor_keyword_assoc_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/doctor-keyword-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_doctor_keyword_assoc_should_return_one(self, client, doctor_A_keyword_A_assoc):
        response = client.get(f'/hospital/v1/doctor-keyword-assocs')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_doctor_keyword_assoc(self, client, doctor_A_hospital_A, doctor_keyword_A):
        data = {
            'doctor': doctor_A_hospital_A.uuid,
            'keyword': doctor_keyword_A.uuid
        }
        response = client.post('/hospital/v1/doctor-keyword-assocs', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.DoctorKeywordAssoc.objects.all().count() == 1


class TestHospitalTreatment:
    @pytest.mark.django_db
    def test_list_hospital_treatment_should_return_zero(self, client):
        response = client.get(f'/hospital/v1/hospital-treatments')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_treatment_should_return_one(self, client, hospital_treatments_test_A):
        response = client.get(f'/hospital/v1/hospital-treatments')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_hospital_treatment(self, client, hospital_test_A):
        data = {
            'name': '도수치료A',
            'hospital': hospital_test_A.uuid,
            'price': 80000,
            'price_per_hour': 160000,
            'description': '원장이 직접 실시'
        }
        response = client.post('/hospital/v1/hospital-treatments', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.HospitalTreatment.objects.all().count() == 1
