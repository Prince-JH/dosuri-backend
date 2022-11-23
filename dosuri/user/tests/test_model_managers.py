import pytest

from dosuri.user import models as um


class TestUser:
    @pytest.mark.django_db
    def test_create_user_if_not_exist(self):
        user, is_new = um.User.objects.get_or_create_user('test')

        assert is_new is True
        assert um.User.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_user_if_exist(self, user_dummy):
        user, is_new = um.User.objects.get_or_create_user('dummy@dummy.com')

        assert is_new is False
        assert um.User.objects.all().count() == 1
