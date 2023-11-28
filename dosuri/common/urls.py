from django.contrib import admin
from django.urls import path, include

from dosuri.common import views as cv

urlpatterns = [
    path('v1/addresses', cv.AddressList.as_view(), name='address-list'),
    path('v1/addresses/<uuid>', cv.AddressDetail.as_view(), name='address-detail'),
    path('v1/attachment', cv.Attachment.as_view(), name='attachment'),
    path('v1/attachment/<uuid>', cv.AttachmentDetail.as_view(), name='attachment-detail'),
    path('v1/relocation', cv.rotation_review_view, name='relocation-article'),
]
