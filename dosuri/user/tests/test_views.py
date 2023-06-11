import json

import pytest
import requests_mock
from django.contrib.auth import get_user_model

from dosuri.user import (
    models as um,
    constants as uc,
    auth as a,
    mockings as mo
)


class TestUserDetail:
    @pytest.mark.django_db
    def test_get_user_with_jwt(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get(f'/user/v1/users/me', **headers)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_user_without_jwt(self, client, user_dummy):
        response = client.get(f'/user/v1/users/me')
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_create_user_aka_new_join(self, client):
        headers = {
            'content_type': 'application/json'
        }
        data = {
            "username": "igoman2@naver.com",
            "name": "한준호",
            "nickname": "아이고맨",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "name": "별칭",
                "address": "서울특별시 서초구 테헤란로 343",
                "address_type": "etc",
                "latitude": 37.517331925853,
                "longitude": 127.047377408384
            },
            "sex": "남자",
            "pain_areas": [
                {
                    "name": "목"
                },
                {
                    "name": "그 외"
                }
            ]
        }
        response = client.post(f'/user/v1/users', data=data, **headers)
        assert response.status_code == 201

        new_user = get_user_model().objects.all().first()
        assert new_user.name == '한준호'
        assert new_user.nickname == '아이고맨'
        address = um.UserAddress.objects.get(user=new_user)
        assert address.name == '별칭'
        assert address.is_main

    @pytest.mark.django_db
    def test_update_user_aka_join(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        assert user_dummy.name is None

        data = {
            "username": "igoman2@naver.com",
            "name": "한준호",
            "nickname": "아이고맨",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "name": "별칭",
                "address": "서울특별시 서초구 테헤란로 343",
                "address_type": "etc",
                "latitude": 37.517331925853,
                "longitude": 127.047377408384
            },
            "sex": "남자",
            "pain_areas": [
                {
                    "name": "목"
                },
                {
                    "name": "그 외"
                }
            ]
        }
        response = client.put(f'/user/v1/users/me', data=data, **headers)
        assert response.status_code == 200

        user_dummy = get_user_model().objects.get(pk=user_dummy.pk)
        assert user_dummy.name == '한준호'
        assert user_dummy.nickname == '아이고맨'
        address = um.UserAddress.objects.get(user=user_dummy)
        assert address.name == '별칭'
        assert address.is_main

    @pytest.mark.django_db()
    def test_create_user_without_address_should_not_update_user_info(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        assert user_dummy.name is None

        data = {
            "username": "igoman2@naver.com",
            "name": "한준호",
            "nickname": "아이고맨",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "sex": "남자",
            "address": {},
            "pain_areas": [
                {
                    "name": "목"
                },
                {
                    "name": "그 외"
                }
            ]
        }
        response = client.put(f'/user/v1/users/me', data=data, **headers)
        assert response.status_code == 400
        user_dummy = get_user_model().objects.get(pk=user_dummy.pk)
        assert not user_dummy.name
        assert um.UserAddress.objects.filter(user=user_dummy).count() == 0

    @pytest.mark.django_db
    def test_partial_update_user(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        assert user_dummy.name is None

        data = {
            "name": "한준호"
        }
        response = client.patch(f'/user/v1/users/me', data=data, **headers)
        assert response.status_code == 200

        user_dummy = get_user_model().objects.get(pk=user_dummy.pk)
        assert user_dummy.name == '한준호'

    @pytest.mark.django_db
    def test_delete_user(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.delete(f'/user/v1/users/me', **headers)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_user_unread_notice(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get(f'/user/v1/users/me', **headers)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['unread_notice'] is True

        response = client.put(f'/user/v1/users/notice', **headers)
        assert response.status_code == 200

        user_dummy = get_user_model().objects.get(pk=user_dummy.pk)
        assert user_dummy.unread_notice is False

    @pytest.mark.django_db
    def test_partial_update_user_setting(self, client, user_dummy, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        assert user_dummy.name is None

        data = {
            "setting": {
                "agree_marketing_personal_info": False,
            }
        }
        response = client.patch(f'/user/v1/users/me', data=data, **headers)
        assert response.status_code == 200
        assert um.UserSetting.objects.get(user=user_dummy).agree_general_push is True
        assert um.UserSetting.objects.get(user=user_dummy).agree_marketing_personal_info is False


class TestKaKaoAuth:
    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_new_user_should_return_tokens_with_true_is_new(self, client, **kwargs):
        kwargs['mock'].post(f'https://kauth.kakao.com/oauth/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://kapi.kakao.com/v2/user/me', json=mo.kakao_user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'kakao',
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is True
        user = get_user_model().objects.first()
        assert get_user_model().objects.all().count() == 1
        assert user.phone_no == '010-1234-5678'

    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_old_user_should_return_tokens_with_false_is_new(self, client, user_dummy, user_dummy_address_etc,
                                                                  **kwargs):
        kwargs['mock'].post(f'https://kauth.kakao.com/oauth/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://kapi.kakao.com/v2/user/me', json=mo.kakao_user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'kakao'
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is False


class TestGoogleAuth:
    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_new_user_should_return_tokens_with_true_is_new(self, client, **kwargs):
        kwargs['mock'].post(f'https://oauth2.googleapis.com/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://openidconnect.googleapis.com/v1/userinfo', json=mo.google_user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'google',
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is True
        assert get_user_model().objects.all().count() == 1

    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_old_user_should_return_tokens_with_false_is_new(self, client, user_dummy, user_dummy_address_etc,
                                                                  **kwargs):
        kwargs['mock'].post(f'https://oauth2.googleapis.com/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://openidconnect.googleapis.com/v1/userinfo', json=mo.google_user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'google'
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is False


class TestPasswordAuth:
    @pytest.mark.django_db
    def test_auth_correct_password_should_return_tokens(self, client, user_dummy_password):
        data = {
            'username': user_dummy_password.username,
            'password': user_dummy_password.password,
            'type': 'password',
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)
        assert response.status_code == 201
        assert content['is_new'] is True
        assert get_user_model().objects.all().count() == 1

    @pytest.mark.django_db
    def test_auth_wrong_password_should_return_tokens(self, client, user_dummy_password):
        data = {
            'username': user_dummy_password.username,
            'password': 'wrong_password',
            'type': 'password',
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)
        assert response.status_code == 400
        assert content['detail'] == 'Wrong username or password.'


class TestUserNickname:
    @pytest.mark.django_db
    def test_not_duplicated_nickname(self, client):
        response = client.get('/user/v1/users/nickname?nickname=dummy')

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_duplicated_nickname(self, client, user_dummy):
        response = client.get('/user/v1/users/nickname?nickname=dummy')

        assert response.status_code == 409

    @pytest.mark.django_db
    def test_check_given_name_duplicated(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/nickname?nickname=dummy', **headers)

        assert response.status_code == 200


class TestInsuranceUserAssoc:
    @pytest.mark.django_db
    def test_create_request_within_day(self, client, celery_app, celery_config, tokens_user_dummy,
                                       insurance_user_assoc_new, user_dummy_address_서울_main):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        client.post('/user/v1/insurance-user-assocs', **headers)
        assert um.InsuranceUserAssoc.objects.all().count() == 1

    @pytest.mark.django_db
    def test_create_without_address_info(self, client, tokens_user_dummy, insurance_A):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.post('/user/v1/insurance-user-assocs', **headers)

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_anonymous_user(self, client):
        headers = {
            'content_type': 'application/json'
        }
        response = client.post('/user/v1/insurance-user-assocs', **headers)

        assert response.status_code == 401


class TestUserTotalPoint:
    @pytest.mark.django_db
    def test_get_total_point(self, client, tokens_user_dummy, user_dummy_point_history_100):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/me/point', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['total_point'] == 100


class TestUserAddress:
    @pytest.mark.django_db
    def test_list_address_should_return_zero(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/me/addresses', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_address_should_return_one(self, client, tokens_user_dummy, user_dummy_address_home):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/me/addresses', **headers)

        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['results']) == 1

    @pytest.mark.django_db
    def test_create_home_address(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'name': None,
            'address': '수원시 팔달구 아주로 111',
            'address_type': 'home',
            'latitude': 123.123,
            'longitude': 124.124
        }
        response = client.post('/user/v1/users/me/addresses', data=data, **headers)

        assert response.status_code == 201
        assert um.UserAddress.objects.all().count() == 1

    @pytest.mark.django_db
    def test_create_home_address_when_already_exists(self, client, tokens_user_dummy, user_dummy_address_home):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'name': None,
            'address': '수원시 팔달구 아주로 111',
            'address_type': 'home',
            'latitude': 123.123,
            'longitude': 124.124
        }
        response = client.post('/user/v1/users/me/addresses', data=data, **headers)

        assert response.status_code == 201
        content = json.loads(response.content)
        assert content['longitude'] == 124.124

    @pytest.mark.django_db
    def test_create_address_with_invalid_address_type(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'name': None,
            'address': '수원시 팔달구 아주로 111',
            'address_type': 'invalid type',
            'latitude': 123.123,
            'longitude': 124.124
        }
        response = client.post('/user/v1/users/me/addresses', data=data, **headers)

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_address_to_main(self, client, tokens_user_dummy, user_dummy_address_home,
                                    user_dummy_address_office):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'is_main': True
        }
        response = client.patch(f'/user/v1/users/me/addresses/{user_dummy_address_home.uuid}', data=data, **headers)
        user_dummy_address_home.refresh_from_db()
        user_dummy_address_office.refresh_from_db()
        assert response.status_code == 200
        assert user_dummy_address_home.is_main
        assert not user_dummy_address_office.is_main

    @pytest.mark.django_db
    def test_delete_address(self, client, tokens_user_dummy, user_dummy_address_home):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'is_main': True
        }
        response = client.delete(f'/user/v1/users/me/addresses/{user_dummy_address_home.uuid}', data=data, **headers)
        assert response.status_code == 204
        assert um.UserAddress.objects.all().count() == 0


class TestUserPersonalInformationAgreement:
    @pytest.mark.django_db
    def test_get_agreement_when_not_exist(self, client, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/me/personal-info-agreement', **headers)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_agreement_when_exists(self, client, tokens_user_dummy, user_setting):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        response = client.get('/user/v1/users/me/personal-info-agreement', **headers)
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['agree_marketing_personal_info']

    @pytest.mark.django_db
    def test_update_agreement_when_exists(self, client, user_dummy, tokens_user_dummy, user_setting):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        data = {
            'agree_marketing_personal_info': False,
        }
        response = client.patch('/user/v1/users/me/personal-info-agreement', data=data, **headers)
        assert response.status_code == 200
        agreement = um.UserSetting.objects.get(user=user_dummy)
        assert not agreement.agree_marketing_personal_info
