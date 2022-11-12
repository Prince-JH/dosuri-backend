import pytest
from dosuri.user.models import User


@pytest.fixture
def user_A():
    return User.objects.create_user(
        username='A@A.com'
    )
