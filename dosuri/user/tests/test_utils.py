import pytest
from django.contrib.auth import get_user_model

from dosuri.user import utils as uu


class TestRandomNickname:
    @pytest.mark.django_db
    def test_get_random_nickname(self, client, user_dummy):
        assert uu.get_random_nickname('unique') == 'unique'

    @pytest.mark.django_db
    def test_get_random_nickname_duplicated(self, client, user_dummy):
        assert uu.get_random_nickname(user_dummy.nickname) == user_dummy.nickname + '1'

    @pytest.mark.django_db
    def test_get_random_nickname_duplicated_twice(self, client, user_dummies):
        assert get_user_model().objects.all().count() == 100
        nickname = uu.get_random_nickname('dummy')
        assert bool('dummy' not in nickname)

