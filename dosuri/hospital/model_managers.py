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