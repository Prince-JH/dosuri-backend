from django.contrib.auth.models import UserManager
from django.db.models import Manager


class DosuriUserManager(UserManager):
    def get_user_by_uuid(self, uuid):
        return self.get(uuid=uuid)

    def update_user_info(self, user, user_info):
        self.filter(pk=user.pk).update(**user_info)


class UserPointHistoryManager(Manager):
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

    def get_total_point(self, user):
        qs = self.filter(user=user)
        return qs.order_by('-created_at').first().total_point if qs.exists() else 0


class UserNotificationManager(Manager):
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


class AddressUserAssocManager(Manager):
    def get_user_address(self, user):
        try:
            address = self.get(user=user).address
            return f'{address.large_area}{address.small_area}'
        except self.model.DoesNotExist:
            return
