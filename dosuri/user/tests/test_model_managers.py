import pytest

from dosuri.user import (
    models as um,
    constants as uc,
    exceptions as uexc,
)


class TestUser:
    @pytest.mark.django_db
    def test_create_user_if_not_exist(self):
        user = um.User.objects.get_or_create(username='test')[0]

        assert um.User.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_user_if_exist(self, user_dummy):
        um.User.objects.get_or_create(username='dummy@dummy.com')[0]

        assert um.User.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_user_if_exist_and_save_detail(self, user_dummy, assoc_address_수원_user_dummy):
        um.User.objects.get_or_create(username='dummy@dummy.com')[0]

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


class TestUserAddressManager:
    @pytest.mark.django_db
    def test_create_home_address(self, user_dummy):
        um.UserAddress.objects.create_home_address(user_dummy, 'home', '수원시 팔달구 아주로 17', 123.123, 123.123)

        assert um.UserAddress.objects.all().count() == 1
        assert um.UserAddress.objects.all().first().address_type == uc.ADDRESS_HOME

    @pytest.mark.django_db
    def test_create_home_address_when_already_exists(self, user_dummy, user_dummy_address_home):
        with pytest.raises(uexc.HomeAddressExists):
            um.UserAddress.objects.create_home_address(user_dummy, 'home', '수원시 팔달구 아주로 17', 123.123, 123.123)

    @pytest.mark.django_db
    def test_create_office_address(self, user_dummy):
        um.UserAddress.objects.create_office_address(user_dummy, 'office', '서초대로 343 신덕빌딩', 123.123, 123.123)

        assert um.UserAddress.objects.all().count() == 1
        assert um.UserAddress.objects.all().first().address_type == uc.ADDRESS_OFFICE

    @pytest.mark.django_db
    def test_create_home_address_when_already_exists(self, user_dummy, user_dummy_address_office):
        with pytest.raises(uexc.OfficeAddressExists):
            um.UserAddress.objects.create_office_address(user_dummy, 'office', '서초대로 343 신덕빌딩', 123.123, 123.123)

    @pytest.mark.django_db
    def test_create_etc_address_when_already_exists(self, user_dummy, user_dummy_address_etc):
        um.UserAddress.objects.create_etc_address(user_dummy, 'etc', '집앞', 123.123, 123.123)

        assert um.UserAddress.objects.all().count() == 2
