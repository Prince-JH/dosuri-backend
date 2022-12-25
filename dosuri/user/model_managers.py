from django.contrib.auth.models import UserManager
from dosuri.user import models as um


class DosuriUserManager(UserManager):
    def get_or_create_user(self, username):
        try:
            user = self.get(username=username)
            qs = um.AddressUserAssoc.objects.filter(user=user)
            is_new = False if qs.exists() else True
        except um.User.DoesNotExist:
            user = self.create_user(username=username)
            is_new = True
        return user, is_new
