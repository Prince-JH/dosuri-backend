import pytest

from dosuri.common import models as cm
from dosuri.hospital import (
    models as hm,
    constants as hc
)
from dosuri.community import (
    models as cmm,
    constants as cmc
)
from dosuri.user.auth import get_tokens_for_user
from dosuri.user.models import User

@pytest.fixture
def user_dummy():
    return User.objects.create_user(
        username='dummy@dummy.com',
        nickname='dummy'
    )
    
@pytest.fixture
def hospital_test_A():
    return hm.Hospital.objects.create(
        name='test_A'
    )
    
@pytest.fixture
def treatmeny_keyword_A():
    return cmm.TreatmentKeyword.objects.create(keyword="도수치료")