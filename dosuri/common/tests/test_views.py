import json

import pytest

from dosuri.hospital import (
    models as hm,
    constants as hc
)
from dosuri.common import (
    models as cm,
)


class TestAddress:
    @pytest.mark.django_db
    def test_list_address_by_uuid_sets_should_return_two(self, client, assoc_hospital_A_address_강남,
                                                              assoc_hospital_B_address_수원,
                                                              hospital_test_A, hospital_test_B, address_서울시_강남구,
                                                              address_수원시_팔달구):
        response = client.get(
            f'/common/v1/addresses/?uuid_set={address_서울시_강남구.uuid}&uuid_set={address_수원시_팔달구.uuid}')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 2
