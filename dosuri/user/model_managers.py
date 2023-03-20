from django.contrib.auth.models import UserManager
from django.db.models import Manager
from dosuri.user import (
    constants as uc,
    exceptions as uexc,
)


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

    def give_point(self, user, point, content):
        self.create_history(user, point, content)

    def take_pint(self, user, point, content):
        self.create_history(user, -point, content)

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


class UserAddressManager(Manager):
    def create_address(self, data):
        if data['address_type'] == uc.ADDRESS_HOME:
            instance = self.create_home_address(user=data['user'],
                                                name=data['name'],
                                                address=data['address'],
                                                latitude=data['latitude'],
                                                longitude=data['longitude'])

        elif data['address_type'] == uc.ADDRESS_OFFICE:
            instance = self.create_office_address(user=data['user'],
                                                  name=data['name'],
                                                  address=data['address'],
                                                  latitude=data['latitude'],
                                                  longitude=data['longitude'])
        else:
            instance = self.create_etc_address(user=data['user'],
                                               name=data['name'],
                                               address=data['address'],
                                               latitude=data['latitude'],
                                               longitude=data['longitude'])
        return instance

    def create_home_address(self, user, name, address, latitude, longitude):
        if self.filter(user=user, address_type=uc.ADDRESS_HOME).exists():
            raise uexc.HomeAddressExists()
        return self.create(user=user, name=name, address=address, address_type=uc.ADDRESS_HOME, latitude=latitude,
                           longitude=longitude)

    def create_office_address(self, user, name, address, latitude, longitude):
        if self.filter(user=user, address_type=uc.ADDRESS_OFFICE).exists():
            raise uexc.OfficeAddressExists()
        return self.create(user=user, name=name, address=address, address_type=uc.ADDRESS_OFFICE, latitude=latitude,
                           longitude=longitude)

    def create_etc_address(self, user, name, address, latitude, longitude):
        return self.create(user=user, name=name, address=address, address_type=uc.ADDRESS_ETC, latitude=latitude,
                           longitude=longitude)
