import pytest

from dosuri.user import models as um


class TestUser:
    @pytest.mark.django_db
    def test_create_user_if_not_exist(self):
        user = um.User.objects.get_or_create(username='test')[0]

        assert um.User.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_user_if_exist(self, user_dummy):
        user = um.User.objects.get_or_create(username='dummy@dummy.com')[0]

        assert um.User.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_user_if_exist_and_save_detail(self, user_dummy, assoc_address_수원_user_dummy):
        user = um.User.objects.get_or_create(username='dummy@dummy.com')[0]

        assert um.User.objects.all().count() == 1


class TestUserPointHistory:
    @pytest.mark.django_db
    def test_create_history(self, user_dummy):
        um.UserPointHistory.objects.create_history(user_dummy, 100, 'test')

        assert um.UserPointHistory.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_total_point(self, user_dummy):
        um.UserPointHistory.objects.create_history(user_dummy, 100, 'test')
        total_point = um.UserPointHistory.objects.get_total_point(user_dummy)

        assert total_point

