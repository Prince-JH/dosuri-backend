from django.contrib.auth.models import UserManager
from dosuri.user import models as um


class DosuriUserManager(UserManager):
    def get_or_create_user(self, username):
        try:
            user = self.get(username=username)
            is_new = False
        except um.User.DoesNotExist:
            user = self.create_user(username=username)
            is_new = True
        return user, is_new
