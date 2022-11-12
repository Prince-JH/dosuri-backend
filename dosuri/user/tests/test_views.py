import json

import pytest

from dosuri.user import (
    models as um,
    constants as uc
)


class TestUserList:
    @pytest.mark.django_db
    def test_list_user_should_return_zero(self, client):
        response = client.get('/user/v1/users/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_list_user_should_return_one_result(self, client, user_A):
        response = client.get('/user/v1/users/')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 1


class TestUserDetail:
    @pytest.mark.django_db
    def test_get_user_by_uuid(self, client, user_A):
        response = client.get(f'/user/v1/users/{user_A.uuid}/')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['username'] == user_A.username


class TestKaKaoAuth:
    @pytest.mark.django_db
    def test_auth_new_user_should_return_tokens_with_true_is_new(self, client):
        data = {
            'token': 'dummy_token',
            'username': 'dummy@dummy.com',
            'type': 'kakao',
        }
        response = client.post('/user/v1/auth/', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is True

    @pytest.mark.django_db
    def test_auth_old_user_should_return_tokens_with_false_is_new(self, client, user_A):
        data = {
            'token': 'dummy_token',
            'username': 'A@A.com',
            'type': 'kakao'
        }
        response = client.post('/user/v1/auth/', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is False
