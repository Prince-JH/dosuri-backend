from django.contrib import admin

from dosuri.common import models as cm
from dosuri.community import models as cmm
from dosuri.user import models as um
from dosuri.hospital import models as hm

admin.site.register(cm.Address)
admin.site.register(hm.Hospital)
admin.site.register(hm.HospitalImage)
admin.site.register(hm.HospitalTreatment)
admin.site.register(hm.HospitalCalendar)
admin.site.register(hm.HospitalKeyword)
admin.site.register(hm.DoctorKeyword)
admin.site.register(hm.HospitalKeywordAssoc)
admin.site.register(hm.Doctor)
admin.site.register(hm.DoctorDescription)
admin.site.register(hm.DoctorKeywordAssoc)

admin.site.register(um.User)
