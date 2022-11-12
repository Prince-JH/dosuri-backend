from django.db.models import Manager

from dosuri.common import models as cm


class AddressManager(Manager):
    def get_uuid_by_id(self, address_id):
        if not address_id or address_id == '':
            return ''
        try:
            return self.get(id=address_id).uuid
        except cm.Address.DoesNotExist:
            return ''
