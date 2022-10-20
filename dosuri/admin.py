from django.contrib import admin
from dosuri.user.models import User
from dosuri.hospital import models as hm


class AddressAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'do', 'city', 'gun', 'gu')
    readonly_fields = ('uuid', 'created_at')


admin.site.register(hm.Address, AddressAdmin)

admin.site.register(User)
