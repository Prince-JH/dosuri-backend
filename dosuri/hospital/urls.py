from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('v1/hospitals/', v.HospitalList.as_view(), name='hospital-list'),
    path('v1/hospitals/<uuid>/', v.HospitalDetail.as_view(), name='hospital-detail'),
    path('v1/hospitals-calendar/', v.HospitalCalendarList.as_view(), name='hospital-calendar'),
    path('v1/hospitals-calendar/<uuid>/', v.HospitalCalendarDetail.as_view(), name='hospital-calendar-detail'),
]
