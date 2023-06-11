from django.core.management.base import BaseCommand

from dosuri.common.geocoding import KaKaoGeoClient
from dosuri.hospital.models import Hospital
from django.core.management.base import BaseCommand

from dosuri.user import (
    models as um
)


class Command(BaseCommand):
    help = 'Get users default setting'

    def handle(self, *args, **options):
        set_user_default_setting()


def set_user_default_setting():
    users = um.User.objects.filter(is_real=True)
    for user in users:
        print(user)
        qs = um.UserSetting.objects.filter(user=user)
        if not qs.exists():
            um.UserSetting.objects.create_default_setting(user)
