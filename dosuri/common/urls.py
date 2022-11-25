from django.contrib import admin
from django.urls import path, include

from dosuri.common import views as cv

urlpatterns = [
    path('v1/addresses/<uuid>/', cv.AddressDetail.as_view(), name='address-detail'),

]