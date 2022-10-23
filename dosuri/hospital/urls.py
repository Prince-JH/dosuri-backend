from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('hospitals/', v.HospitalList.as_view(), name='hospital-list'),
    path('hospitals/<uuid>', v.HospitalDetail.as_view(), name='hospital-detail'),
]
