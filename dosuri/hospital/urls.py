from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('v1/hospitals', v.HospitalList.as_view(), name='hospital'),
    path('v1/hospitals/<uuid>', v.HospitalDetail.as_view(), name='hospital-detail'),
    path('v1/hospital-calendars', v.HospitalCalendarList.as_view(), name='hospital-calendar'),
    path('v1/hospital-calendars/<uuid>', v.HospitalCalendarDetail.as_view(), name='hospital-calendar-detail'),
    path('v1/hospital-images', v.HospitalImageList.as_view(), name='hospital-image'),
    path('v1/hospital-images/<uuid>', v.HospitalImageDetail.as_view(), name='hospital-image-detail'),
    path('v1/hospital-address-assocs', v.HospitalAddressAssocList.as_view(), name='hospital-address-assoc'),
    path('v1/hospital-address-assocs/<uuid>', v.HospitalAddressAssocDetail.as_view(),
         name='hospital-address-assoc-detail'),
    path('v1/doctors', v.DoctorList.as_view(), name='doctor'),
    path('v1/doctors/<uuid>', v.DoctorDetail.as_view(), name='doctor-detail'),
    path('v1/doctor-descriptions', v.DoctorDescriptionList.as_view(), name='doctor-description'),
    path('v1/doctor-descriptions/<uuid>', v.DoctorDescriptionDetail.as_view(), name='doctor-description-detail'),
    path('v1/hospital-keywords', v.HospitalKeywordList.as_view(), name='hospital-keyword'),
    path('v1/hospital-keywords/<uuid>', v.HospitalKeywordDetail.as_view(), name='hospital-keyword-detail'),
    path('v1/doctor-keywords', v.DoctorKeywordList.as_view(), name='doctor-keyword'),
    path('v1/doctor-keywords/<uuid>', v.DoctorKeywordDetail.as_view(), name='doctor-keyword-detail'),
    path('v1/hospital-keyword-assocs', v.HospitalKeywordAssocList.as_view(), name='hospital-keyword-assoc'),
    path('v1/hospital-keyword-assocs/<uuid>', v.HospitalKeywordAssocList.as_view(),
         name='hospital-keyword-assoc-detail'),
    path('v1/doctor-keyword-assocs', v.DoctorKeywordAssocList.as_view(), name='doctor-keyword-assoc'),
    path('v1/doctor-keyword-assocs/<uuid>', v.DoctorKeywordAssocDetail.as_view(), name='doctor-keyword-assoc-detail'),
    path('v1/hospital-treatments', v.HospitalTreatmentList.as_view(), name='hospital-treatments'),
    path('v1/hospital-treatments/<uuid>', v.HospitalTreatmentDetail.as_view(), name='hospital-treatments'),

]
