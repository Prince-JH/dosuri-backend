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
    def test_update_user(self, client, user_dummy, tokens_user_dummy):
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
                "large_area": "서울",
                "small_area": "강남구"
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
    def test_delete_user(self, client):
        response = client.get(f'/user/v1/users/me')
        assert response.status_code == 401


class TestKaKaoAuth:
    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_new_user_should_return_tokens_with_true_is_new(self, client, **kwargs):
        kwargs['mock'].post(f'https://kauth.kakao.com/oauth/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://kapi.kakao.com/v2/user/me', json=mo.user_info_data)
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
    def test_auth_old_user_should_return_tokens_with_false_is_new(self, client, user_dummy, assoc_address_수원_user_dummy,
                                                                  **kwargs):
        kwargs['mock'].post(f'https://kauth.kakao.com/oauth/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://kapi.kakao.com/v2/user/me', json=mo.user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'kakao'
        }
        response = client.post('/user/v1/auth', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is False


class TestUserNickname:
    @pytest.mark.django_db
    def test_not_duplicated_nickname(self, client):
        response = client.get('/user/v1/users/nickname?nickname=dummy')

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_duplicated_nickname(self, client, user_dummy):
        response = client.get('/user/v1/users/nickname?nickname=dummy')

        assert response.status_code == 409


class TestInsuranceUserAssoc:
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
