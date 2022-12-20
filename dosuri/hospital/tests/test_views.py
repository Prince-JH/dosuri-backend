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

    # @pytest.mark.django_db
    # def test_create_hospital(self, client, address_서울시_강남구):
    #     data = {
    #         'address': address_서울시_강남구.uuid,
    #         'name': 'test hospital',
    #         'introduction': None,
    #         'phone_no': None,
    #         'is_partner': False,
    #         'opened_at': None,
    #         'area': None
    #     }
    #     response = client.post('/hospital/v1/hospitals', data=data, content_type='application/json')
    #
    #     assert response.status_code == 201
    #     assert hm.Hospital.objects.all().count() == 1

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


# class TestHospitalDetail:
#     @pytest.mark.django_db
#     def test_get_hospital_by_uuid(self, client, hospital_test_A):
#         response = client.get(f'/hospital/v1/hospitals/{hospital_test_A.uuid}')
#         content = json.loads(response.content)
#         assert response.status_code == 200
#         assert content['name'] == hospital_test_A.name


# class TestDoctor:
    # @pytest.mark.django_db
    # def test_doctor_list_by_position(
    #         self, client, doctor_A_hospital_A, therapist_A_hospital_A):
    #     response = client.get('/hospital/v1/doctors?position=doctor', content_type='application/json')
    #     content = json.loads(response.content)
    #     assert len(content['results']) == 1
    #     assert content['results'][0]['position'] == 'doctor'
    #
    #     response = client.get('/hospital/v1/doctors?position=therapist', content_type='application/json')
    #     content = json.loads(response.content)
    #     assert len(content['results']) == 1
    #     assert content['results'][0]['position'] == 'therapist'
#     @pytest.mark.django_db
#     def test_create_doctor(self, client, hospital_test_A):
#         data = {
#             'hospital': hospital_test_A.uuid,
#             'name': 'test doctor',
#             'thumbnail_url': None,
#             'title': 'chief',
#             'subtitle': 'chief',
#             'position': 'therapist',
#         }
#         response = client.post('/hospital/v1/doctors', data=data, content_type='application/json')
#
#         assert response.status_code == 201
#         assert hm.Hospital.objects.all().count() == 1


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


class TestHospitalUserAssoc:
    @pytest.mark.django_db
    def test_create_hospital_treatment(self, client, hospital_test_A, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'hospital': hospital_test_A.uuid,
            'is_up': True
        }
        response = client.post('/hospital/v1/hospital-user-assocs', data=data, **headers)

        assert response.status_code == 201
        assert hm.HospitalUserAssoc.objects.all().count() == 1
        assert hm.HospitalUserAssoc.objects.first().is_up

        client.post('/hospital/v1/hospital-user-assocs', data=data, **headers)
        assert hm.HospitalUserAssoc.objects.all().count() == 1


class TestHospitalSearch:
    @pytest.mark.django_db
    def test_create_hospital_search(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'word': 'value'
        }
        response = client.post('/hospital/v1/hospital-searches', data=data, **headers)

        assert response.status_code == 201
        assert hm.HospitalSearch.objects.all().count() == 1
        search = hm.HospitalSearch.objects.all().first()
        assert search.user == user_dummy
        assert search.word == 'value'

    @pytest.mark.django_db
    def test_list_hospital_searches(self, client, tokens_user_dummy, hospital_search_A_user_dummy,
                                    hospital_search_B_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/hospital/v1/hospital-searches', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)

        assert len(content['results']) == 2
        assert content['results'][0]['word'] == 'B'
