from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.common import models as cm
from dosuri.hospital import (
    models as m,
    serializers as s
)
from dosuri.common import filters as f


class AddressDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Address.objects.all()
    serializer_class = s.Address
    lookup_field = 'uuid'


# Todo verification 로직 타기
class HospitalList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.select_related('address').all()
    serializer_class = s.Hospital
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, rf.SearchFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name']
    uuid_filter_params = ['address']


class HospitalDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all()
    serializer_class = s.Hospital
    lookup_field = 'uuid'


class HospitalCalendarList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalCalendar.objects.select_related('hospital').all()
    serializer_class = s.HospitalCalendar
    filter_backends = [f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']


class HospitalCalendarDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalCalendar.objects.all()
    serializer_class = s.HospitalCalendar
    lookup_field = 'uuid'


class HospitalImageList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalImage.objects.select_related('hospital').all()
    serializer_class = s.HospitalImage
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class HospitalImageDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalImage.objects.all()
    serializer_class = s.HospitalImage
    lookup_field = 'uuid'


class DoctorList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Doctor.objects.select_related('hospital').all()
    serializer_class = s.Doctor
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class DoctorDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Doctor.objects.all()
    serializer_class = s.Doctor
    lookup_field = 'uuid'


class DoctorDescriptionList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.select_related('doctor').all()
    serializer_class = s.DoctorDescription
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor']


class DoctorDescriptionDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    lookup_field = 'uuid'


class KeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Keyword.objects.all()
    serializer_class = s.Keyword
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class KeywordDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Keyword.objects.all()
    serializer_class = s.Keyword
    lookup_field = 'uuid'


class HospitalKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeywordAssoc.objects.select_related('hospital', 'keyword').all()
    serializer_class = s.HospitalKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital', 'keyword']


class HospitalKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeywordAssoc.objects.all()
    serializer_class = s.HospitalKeywordAssoc
    lookup_field = 'uuid'


class DoctorKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorKeywordAssoc.objects.select_related('doctor', 'keyword').all()
    serializer_class = s.DoctorKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor', 'keyword']


class DoctorKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorKeywordAssoc.objects.all()
    serializer_class = s.DoctorKeywordAssoc
    lookup_field = 'uuid'


class HospitalTreatmentList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalTreatment.objects.select_related('hospital').all()
    serializer_class = s.HospitalTreatment
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class HospitalTreatmentDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalTreatment.objects.all()
    serializer_class = s.HospitalTreatment
    lookup_field = 'uuid'
