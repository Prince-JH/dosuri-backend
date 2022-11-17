import json

import pytest

from dosuri.user import (
    models as um,
    constants as uc,
    auth as a
)


class TestUserDetail:
    @pytest.mark.django_db
    def test_get_user_without_jwt(self, client):
        response = client.get(f'/user/v1/users/me')
        assert response.status_code == 401


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
