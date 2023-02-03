from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('v1/hospitals', v.HospitalList.as_view(), name='hospital'),
    path('v1/temp-hospitals', v.TempHospital.as_view(), name='temp-hospital'),
    path('v1/hospitals/home', v.HomeHospitalList.as_view(), name='hospital-home'),
    path('v1/hospitals-address-filtered', v.HospitalAddressFilteredList.as_view(), name='hospital-address-filtered'),
    path('v1/hospitals-address-filtered-avg-price', v.HospitalAddressFilteredAvgPriceList.as_view(),
         name='hospital-address-filtered-avg-price'),
    path('v1/hospitals-current-address-filtered-avg-price', v.HospitalCurrentAddressFilteredAvgPriceList.as_view(),
         name='hospital-address-filtered-avg-price'),
    path('v1/hospitals-current-address-filtered', v.HospitalCurrentAddressFilteredList.as_view(),
         name='hospital-current-address-filtered'),
    path('v1/hospitals/<uuid>', v.HospitalDetail.as_view(), name='hospital-detail'),

    path('v1/hospital-address-assocs', v.HospitalAddressAssocList.as_view(), name='hospital-address-assoc'),
    path('v1/hospital-address-assocs/<uuid>', v.HospitalAddressAssocDetail.as_view(),
         name='hospital-address-assoc-detail'),

    path('v1/hospital-user-assocs', v.HospitalUserAssoc.as_view(),
         name='hospital-user-assoc'),

    path('v1/doctors', v.DoctorList.as_view(), name='doctor'),
    path('v1/doctors/<uuid>', v.DoctorDetail.as_view(), name='doctor-detail'),

    path('v1/hospital-treatments', v.HospitalTreatmentList.as_view(), name='hospital-treatment'),
    path('v1/hospital-treatments/<uuid>', v.HospitalTreatmentDetail.as_view(), name='hospital-treatment-detail'),

    path('v1/hospital-searches', v.HospitalSearch.as_view(), name='hospital-search'),
    path('v1/hospital-searches/<uuid>', v.HospitalSearchDetail.as_view(), name='hospital-search-detail'),
]
