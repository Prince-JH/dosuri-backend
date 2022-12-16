from django.contrib import admin
from django.urls import path, include

from dosuri.hospital import views as v

urlpatterns = [

    path('v1/hospitals', v.HospitalList.as_view(), name='hospital'),
    path('v1/hospitals/<uuid>', v.HospitalDetail.as_view(), name='hospital-detail'),

    path('v1/hospital-address-assocs', v.HospitalAddressAssocList.as_view(), name='hospital-address-assoc'),
    path('v1/hospital-address-assocs/<uuid>', v.HospitalAddressAssocDetail.as_view(),
         name='hospital-address-assoc-detail'),

    path('v1/hospital-user-assocs', v.HospitalUserAssoc.as_view(),
         name='hospital-user-assoc'),

    path('v1/doctors', v.DoctorList.as_view(), name='doctor'),
    path('v1/doctors/<uuid>', v.DoctorDetail.as_view(), name='doctor-detail'),

    path('v1/hospital-treatments', v.HospitalTreatmentList.as_view(), name='hospital-treatments'),
    path('v1/hospital-treatments/<uuid>', v.HospitalTreatmentDetail.as_view(), name='hospital-treatments'),

]
