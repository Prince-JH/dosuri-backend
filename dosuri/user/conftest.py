import pytest
from dosuri.user.models import User


@pytest.fixture
def user_dummy():
    return User.objects.create_user(
        username='dummy@dummy.com'
    )
