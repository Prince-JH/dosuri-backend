from django.contrib import admin
from django import forms

from dosuri.common import models as cm
from dosuri.community import models as cmm
from dosuri.user import models as um
from dosuri.hospital import models as hm

admin.site.register(cm.Address)
admin.site.register(hm.Hospital)
admin.site.register(hm.HospitalTreatment)
admin.site.register(hm.HospitalCalendar)
admin.site.register(hm.HospitalKeyword)
admin.site.register(hm.DoctorKeyword)
admin.site.register(hm.HospitalKeywordAssoc)
admin.site.register(hm.Doctor)
admin.site.register(hm.DoctorDescription)
admin.site.register(hm.DoctorKeywordAssoc)


class ArticleAuthAdminInline(admin.TabularInline):
    model = cmm.ArticleAuth
    extra = 0
    exclude = ('uuid',)

#
# class RelationForm(forms.ModelForm):
#     parent = forms.ChoiceField(required=False,
#                                choices=Relation.objects.values_list('id', 'name'))
#     particle = forms.ChoiceField(required=False,
#                                  choices=Particle.objects.values_list('id', 'content'))
#     media = forms.ChoiceField(required=False,
#                               choices=Media.objects.values_list('id', 'name'))
#
#     class Meta:
#         model = Relation


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleAuthAdminInline]
    raw_id_fields = ['hospital', 'user']
    list_display = ['content', 'user', 'created_at']
    search_fields = ['content']


admin.site.register(cmm.Article, ArticleAdmin)
admin.site.register(cmm.ArticleAuth)

admin.site.register(um.User)
