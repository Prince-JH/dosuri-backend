from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.hospital import (
    models as m,
    serializers as s,
    filters as f
)


# Todo verification 로직 타기
class HospitalList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all()
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
    queryset = m.HospitalCalendar.objects.all()
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
    queryset = m.HospitalImage.objects.all()
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
    queryset = m.Doctor.objects.all()
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
    queryset = m.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor']


class DoctorDescriptionDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    lookup_field = 'uuid'

