import pytest

from dosuri.user.models import User


@pytest.fixture
def dummy_user():
    return User.objects.create_user(
        username='dummy',
        email='dummy@dummy.com',
        password='123'
    )
