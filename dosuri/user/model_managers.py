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

    def get_user_by_uuid(self, uuid):
        return self.get(uuid=uuid)

    def update_user_info(self, user, user_info):
        self.filter(pk=user.pk).update(**user_info)


class UserPointHistoryManager(UserManager):
    def create_history(self, user, point, content):
        qs = self.filter(user=user)
        if qs.exists():
            last_point = qs.order_by('-created_at').first().total_point
        else:
            last_point = 0
        return self.create(
            user=user,
            modify_point=point,
            total_point=last_point + point,
            content=content
        )


class UserNotificationManager(UserManager):
    def create_notification(self, user, content):
        return self.create(
            user=user,
            content=content,
            is_new=True
        )

    def check_notification(self, uuid):
        return self.filter(uuid=uuid).update(
            is_new=False
        )
