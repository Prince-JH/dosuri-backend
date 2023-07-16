import json
from urllib import parse

import pytest
import requests_mock
from django.utils import timezone

from dosuri.hospital import (
    models as hm,
    constants as hc,
    mockings as hmo,
)


class TestHospitalList:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/hospital/v1/hospitals')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_hospital_should_return_one_result(self, client, hospital_test_강남):
        response = client.get('/hospital/v1/hospitals')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_search_by_exist_name_should_return_one(self, client, hospital_test_강남):
        response = client.get(f'/hospital/v1/hospitals?search=test_A')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_list_hospital_search_by_not_exist_name_should_return_zero(self, client, hospital_test_강남):
        response = client.get(f'/hospital/v1/hospitals?search=test_B')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_create_hospital(self, client, attachment_A):
        data = {
            'address': '서울시 강남구 삼성동 106',
            'name': '풍림아파트',
            'introduction': '안녕하세요',
            'phone_no': '02-516-2674',
            'is_partner': False,
            'opened_at': timezone.now(),
            'area': '강남구',
            'latitude': 1,
            'longitude': 2,
            'keywords': [
                {
                    'keyword': '척추'
                },
                {
                    'keyword': '요추'
                }
            ],
            'attachments': [
                {
                    'attachment': attachment_A.uuid
                }
            ],
            'calendar': {
                'monday': '10:00 ~ 20:00',
                'tuesday': '10:00 ~ 20:00',
                'wednesday': '10:00 ~ 20:00',
                'thursday': '10:00 ~ 20:00',
                'friday': '10:00 ~ 20:00',
                'saturday': '10:00 ~ 20:00',
                'sunday': None
            }
        }
        response = client.post('/hospital/v1/hospitals', data=data, content_type='application/json')

        content = json.loads(response.content)
        assert response.status_code == 201
        hospital = hm.Hospital.objects.get(uuid=content['uuid'])
        assert hm.Hospital.objects.all().count() == 1
        assert hm.HospitalKeyword.objects.filter(hospital_keyword_assoc__hospital=hospital).count() == 2
        assert hm.HospitalAttachmentAssoc.objects.filter(hospital=hospital).count() == 1
        assert hm.HospitalCalendar.objects.filter(hospital=hospital).count() == 1

    @pytest.mark.django_db
    def test_create_temp_hospital(self, client):
        data = {
            'name': '이름 없는 고무통 병원',
        }
        response = client.post('/hospital/v1/temp-hospitals', data=data, content_type='application/json')

        content = json.loads(response.content)
        assert response.status_code == 201
        hospital = hm.Hospital.objects.get(uuid=content['uuid'])
        assert hm.Hospital.objects.all().count() == 1

    @pytest.mark.django_db
    def test_hospital_list_order_by_review_count(
            self, client, hospital_test_강남, hospital_test_수원, hospital_test_C, article_A_hospital_A,
            article_B_hospital_A,
            article_A_hospital_B):
        response = client.get('/hospital/v1/hospitals?ordering=-article_count', content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert content['results'][0]['uuid'] == hospital_test_강남.uuid
        assert content['results'][1]['uuid'] == hospital_test_수원.uuid
        assert content['results'][2]['uuid'] == hospital_test_C.uuid

    @pytest.mark.django_db
    def test_hospital_list_order_by_review_new(
            self, client, hospital_test_강남, hospital_test_수원, hospital_test_C, article_A_hospital_A,
            article_B_hospital_A,
            article_A_hospital_B):
        response = client.get('/hospital/v1/hospitals?ordering=-latest_article_created_at',
                              content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert content['results'][0]['uuid'] == hospital_test_수원.uuid
        assert content['results'][1]['uuid'] == hospital_test_강남.uuid
        assert content['results'][2]['uuid'] == hospital_test_C.uuid


class TestAddressFilteredHospitalList:
    @pytest.mark.django_db
    def test_list_hospital_should_return_zero(self, client):
        response = client.get('/hospital/v1/hospitals-address-filtered')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_list_address_filtered_hospital_should_return_one_result(self, client, hospital_test_강남, address_수원시_팔달구,
                                                                     tokens_user_dummy, user_dummy_address_서울_main,
                                                                     **kwargs):
        parsed_address = parse.quote(f'{address_수원시_팔달구.large_area} {address_수원시_팔달구.small_area}')
        kwargs['mock'].get(f'https://dapi.kakao.com/v2/local/search/address.json?query={parsed_address}',
                           json=hmo.수원시_팔달구_coordinates)
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/hospital/v1/hospitals-address-filtered', **headers)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1


class TestHospitalDetail:
    @pytest.mark.django_db
    def test_get_hospital_by_uuid(self, client, hospital_test_강남):
        response = client.get(f'/hospital/v1/hospitals/{hospital_test_강남.uuid}')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['name'] == hospital_test_강남.name
        assert content['latitude'] == hospital_test_강남.latitude
        assert content['longitude'] == hospital_test_강남.longitude


class TestDoctor:
    @pytest.mark.django_db
    def test_doctor_list_by_position(
            self, client, doctor_A_hospital_A, therapist_A_hospital_A):
        response = client.get('/hospital/v1/doctors?position=doctor', content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 1
        assert content['results'][0]['position'] == 'doctor'

        response = client.get('/hospital/v1/doctors?position=therapist', content_type='application/json')
        content = json.loads(response.content)
        assert len(content['results']) == 1
        assert content['results'][0]['position'] == hc.POSITION_THERAPIST

    @pytest.mark.django_db
    def test_create_doctor(self, client, hospital_test_강남, attachment_A):
        data = {
            'hospital': hospital_test_강남.uuid,
            'name': 'test doctor',
            'title': 'chief',
            'subtitle': 'chief',
            'position': hc.POSITION_THERAPIST,
            'keywords': [
                {
                    'keyword': '도수'
                },
                {
                    'keyword': '마취'
                }
            ],
            'attachments': [
                {
                    'attachment': attachment_A.uuid
                }
            ],
            'descriptions': [
                {
                    'description': '세브란스 병원 수련'
                },
                {
                    'description': '진찰 잘함'
                }
            ]
        }
        response = client.post('/hospital/v1/doctors', data=data, content_type='application/json')

        content = json.loads(response.content)
        assert response.status_code == 201
        assert hm.Doctor.objects.all().count() == 1
        doctor = hm.Doctor.objects.get(uuid=content['uuid'])
        assert hm.DoctorKeyword.objects.filter(doctor_keyword_assoc__doctor=doctor).count() == 2
        assert hm.DoctorAttachmentAssoc.objects.filter(doctor=doctor).count() == 1
        assert hm.DoctorDescription.objects.filter(doctor=doctor).count() == 2


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
    def test_create_hospital_treatment(self, client, hospital_test_강남):
        data = {
            'name': '도수치료A',
            'hospital': hospital_test_강남.uuid,
            'price': 80000,
            'price_per_hour': 160000,
            'description': '원장이 직접 실시'
        }
        response = client.post('/hospital/v1/hospital-treatments', data=data, content_type='application/json')

        assert response.status_code == 201
        assert hm.HospitalTreatment.objects.all().count() == 1


class TestHospitalUserAssoc:
    @pytest.mark.django_db
    def test_create_hospital_user_assoc(self, client, hospital_test_강남, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'hospital': hospital_test_강남.uuid,
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

    @pytest.mark.django_db
    def test_delete_hospital_searches(self, client, tokens_user_dummy, hospital_search_A_user_dummy,
                                      hospital_search_B_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.delete('/hospital/v1/hospital-searches', **headers)

        assert response.status_code == 204
        assert hm.HospitalSearch.objects.all().count() == 0


@pytest.mark.skip(reason="Skipping Celery task during testing")
class TestHospitalReservation:
    @pytest.mark.django_db
    def test_create_hospital_reservation(self, client, celery_app, celery_config, hospital_test_강남, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'hospital': hospital_test_강남.uuid,
        }
        response = client.post('/hospital/v1/hospital-reservations', data=data, **headers)

        assert response.status_code == 201
        assert hm.HospitalReservation.objects.all().count() == 1

        client.post('/hospital/v1/hospital-reservations', data=data, **headers)
        assert hm.HospitalReservation.objects.all().count() == 1


class TestHomeHospital:
    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_list_home_hospital_without_token(self, client, hospital_test_강남, address_서울시_강남구, tokens_user_dummy,
                                              user_dummy_address_서울_main, **kwargs):
        parsed_address = parse.quote(f'{address_서울시_강남구.large_area}{address_서울시_강남구.small_area}')
        kwargs['mock'].get(f'https://dapi.kakao.com/v2/local/search/address.json?query={parsed_address}',
                           json=hmo.서울특별시_강남구_coordinates)

        headers = {
            'content_type': 'application/json'
        }
        response = client.get('/hospital/v1/hospitals/home', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['address'] == '강남구'
        assert content['top_hospitals'][0]['uuid'] == hospital_test_강남.uuid

    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_list_home_hospital_with_token(self, client, hospital_test_강남, address_수원시_팔달구,
                                           tokens_user_dummy, user_dummy_address_서울_main,
                                           **kwargs):
        parsed_address = parse.quote(f'{address_수원시_팔달구.large_area} {address_수원시_팔달구.small_area}')
        kwargs['mock'].get(f'https://dapi.kakao.com/v2/local/search/address.json?query={parsed_address}',
                           json=hmo.수원시_팔달구_coordinates)
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/hospital/v1/hospitals-address-filtered', **headers)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1


class TestHospitalName:
    @pytest.mark.django_db
    def test_list_home_hospital_without_token(self, client, hospital_test_강남):
        headers = {
            'content_type': 'application/json'
        }
        response = client.get(f'/hospital/v1/hospitals/names?search=A', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['count'] == 1
        assert content['results'][0]['uuid'] == hospital_test_강남.uuid


class TestHospitalMap:
    @pytest.mark.django_db
    def test_list_hospital_map(self, client, hospital_test_강남, hospital_test_수원):
        headers = {
            'content_type': 'application/json'
        }
        latitude = 37.2762816
        longitude = 127.0433978

        response = client.get(f'/hospital/v1/hospitals/map?distance_range=3&latitude={latitude}&longitude={longitude}',
                              **headers)

        assert response.status_code == 200
