import pytest
from dosuri.user import utils as uu


class TestRandomNickname:
    @pytest.mark.django_db
    def test_get_random_nickname(self, client, user_dummy):
        assert uu.get_random_nickname('unique') == 'unique'

    @pytest.mark.django_db
    def test_get_random_nickname_duplicated(self, client, user_dummy):
        assert uu.get_random_nickname(user_dummy.nickname) == user_dummy.nickname + '1'

