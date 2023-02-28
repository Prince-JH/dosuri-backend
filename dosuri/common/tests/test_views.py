import json

import pytest

from dosuri.common import (
    models as cm,
)


class TestAttachments:
    @pytest.mark.django_db
    def test_update_attachment(self, client, attachment_A):
        data = {
            'path': 'update_path_A',
        }
        client.patch(f'/common/v1/attachment/{attachment_A.uuid}', data=data, content_type='application/json')
        attachment_A.refresh_from_db()
        assert attachment_A.path == 'update_path_A'
