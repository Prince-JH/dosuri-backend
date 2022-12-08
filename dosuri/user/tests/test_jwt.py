import pytest
import json


class TestToken:

    # @pytest.mark.django_db
    # def test_get_token_with_valid_data(self, client, dummy_user):
    #     data = {
    #         "username": dummy_user.username
    #     }
    #     response = client.post('/user/v1/token', data)
    #     content = json.loads(response.content)
    #     assert response.status_code == 200
    #     assert content['access']
    #     assert content['refresh']
    #
    #
    # @pytest.mark.django_db
    # def test_verify_valid_token(self, client, dummy_user):
    #     data = {
    #         "username": dummy_user.username
    #     }
    #     response = client.post('/user/v1/token', data)
    #     content = json.loads(response.content)
    #     assert response.status_code == 200

        # response = client.post('/user/v1/token/verify', {'token': content['access']})
        # assert response.status_code == 200

    @pytest.mark.django_db
    def test_verify_invalid_token(self, client):
        response = client.post('/user/v1/token/verify', {'token': 'invalid_token'})
        assert response.status_code == 401

    # @pytest.mark.django_db
    # def test_refresh_with_valid_token(self, client, dummy_user):
    #     data = {
    #         "username": dummy_user.username
    #     }
    #     response = client.post('/user/v1/token', data)
    #     content = json.loads(response.content)
    #     assert response.status_code == 200
    #
    #     response = client.post('/user/v1/token/refresh', {'refresh': content['refresh']})
    #     assert response.status_code == 200
    #     content = json.loads(response.content)
    #     assert content['access']

    @pytest.mark.django_db
    def test_refresh_with_invalid_token(self, client):
        response = client.post('/user/v1/token/refresh', {'refresh': 'invalid_token'})
        assert response.status_code == 401
