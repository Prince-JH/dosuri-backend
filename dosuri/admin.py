from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from dosuri.common import (
    models as cm,
    utils as cu,
)
from dosuri.community import (
    models as cmm,
    constants as cmc,
)
from dosuri.user import models as um
from dosuri.hospital import models as hm

admin.site.register(cm.Address)
admin.site.register(cm.Attachment)
admin.site.register(cmm.ArticleAttachmentAssoc)
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
    list_display = ['content', 'image_preview', 'user', 'created_at', 'is_authenticated']
    search_fields = ['content']
    actions = ['authenticate']

    def authenticate(self, request, queryset):
        for article in queryset:
            article.authenticate_article()

    def is_authenticated(self, obj):
        return True if obj.article_auth.status == cmc.STATUS_COMPLETE else False

    def image_preview(self, obj):
        images = cm.Attachment.objects.filter(auth_attachment_assoc__article_auth__article=obj)
        if len(images) == 0:
            return
        return mark_safe('<img src = "{url}" width = "100" height = "100"/>'.format(
            url=cu.generate_signed_path(images[0])))

    authenticate.short_description = '후기 인증'
    is_authenticated.short_description = '인증 여부'
    image_preview.allow_tags = True


admin.site.register(cmm.Article, ArticleAdmin)
admin.site.register(cmm.ArticleAuth)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nickname', 'created_at']
    search_fields = ['username', 'nickname']


admin.site.register(um.User, UserAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'address_type', 'is_main']
    raw_id_fields = ['user']


admin.site.register(um.UserAddress, UserAddressAdmin)
