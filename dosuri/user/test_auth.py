import pytest

from dosuri.user import auth as a


class TestSocialAuth:
    def test_create_instance(self):
        auth_factory = a.SocialAuth()
        assert type(auth_factory) == a.SocialAuth
