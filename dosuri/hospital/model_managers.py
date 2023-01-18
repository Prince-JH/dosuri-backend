from django.contrib.auth.models import AnonymousUser
from django.db.models import Manager
from dosuri.hospital import model_querysets as mqs


class HospitalUserAssocManager(Manager):
    def press_up_button(self, hospital, user, is_up):
        assoc = self.filter(hospital=hospital, user=user)
        if assoc.exists():
            assoc.update(is_up=is_up)
        else:
            self.create(hospital=hospital, user=user, is_up=is_up)


class HospitalManager(Manager):
    def get_queryset(self):
        return mqs.HospitalQuerySet(self.model, using=self._db)


class HospitalSearchManager(Manager):
    def save_search(self, user, word):
        if isinstance(user, AnonymousUser):
            return
        return self.create(
            user=user,
            word=word
        )


class HospitalKeywordManager(Manager):
    def get_or_create(self, name):
        qs = self.filter(name=name)
        if qs.exists():
            return qs.first()
        return self.create(name=name, is_custom=True)
