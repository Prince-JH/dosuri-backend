from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('v1/hospitals/', v.HospitalList.as_view(), name='hospital'),
    path('v1/hospitals/<uuid>/', v.HospitalDetail.as_view(), name='hospital-detail'),
    path('v1/hospital-calendars/', v.HospitalCalendarList.as_view(), name='hospital-calendar'),
    path('v1/hospital-calendars/<uuid>/', v.HospitalCalendarDetail.as_view(), name='hospital-calendar-detail'),
    path('v1/hospital-images/', v.HospitalImageList.as_view(), name='hospital-image'),
    path('v1/hospital-images/<uuid>/', v.HospitalImageDetail.as_view(), name='hospital-image-detail'),
    path('v1/doctors/', v.DoctorList.as_view(), name='doctor'),
    path('v1/doctors/<uuid>/', v.DoctorDetail.as_view(), name='doctor-detail'),
    path('v1/doctor-descriptions/', v.DoctorDescriptionList.as_view(), name='doctor-description'),
    path('v1/doctor-descriptions/<uuid>/', v.DoctorDescriptionDetail.as_view(), name='doctor-description-detail'),
]
