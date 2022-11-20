import json

import pytest
import requests_mock

from dosuri.user import (
    models as um,
    constants as uc,
    auth as a,
    mockings as mo
)


class TestUserDetail:
    @pytest.mark.django_db
    def test_get_user_without_jwt(self, client):
        response = client.get(f'/user/v1/users/me/')
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
        response = client.post('/user/v1/auth/', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is True

    @pytest.mark.django_db
    @requests_mock.Mocker(kw='mock')
    def test_auth_old_user_should_return_tokens_with_false_is_new(self, client, user_dummy, **kwargs):
        kwargs['mock'].post(f'https://kauth.kakao.com/oauth/token', json=mo.access_token_data)
        kwargs['mock'].get(f'https://kapi.kakao.com/v2/user/me', json=mo.user_info_data)
        data = {
            'token': 'dummy_token',
            'type': 'kakao'
        }
        response = client.post('/user/v1/auth/', data=data, content_type='application/json')
        content = json.loads(response.content)

        assert response.status_code == 201
        assert content['is_new'] is False
