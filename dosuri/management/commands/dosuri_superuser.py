import os
from django.core.management.base import BaseCommand
from dosuri.user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='dosuri').exists():
            User.objects.create_superuser('dosuri', password='dosuri')
