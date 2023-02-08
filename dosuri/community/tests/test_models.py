import pytest

from dosuri.user import models as um
from dosuri.community import (
    models as cmm,
    constants as cmc,
)


class TestArticleModel:
    @pytest.mark.django_db
    def test_authenticate_article(self, user_dummy, article_A_hospital_B, article_auth_A_article_A_hospital_B):
        article_A_hospital_B.authenticate_article()
        point = um.UserPointHistory.objects.get_total_point(user_dummy)

        assert point == 1000
        assert article_auth_A_article_A_hospital_B.status == cmc.STATUS_COMPLETE
