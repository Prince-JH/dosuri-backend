from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.hospital import (
    models as m,
    serializers as s,
    filters as hf
)


# Todo verification 로직 타기
class HospitalList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]

    queryset = m.Hospital.objects.all()
    serializer_class = s.Hospital
    filter_backends = [rf.OrderingFilter, hf.ForeignUuidFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    uuid_filter_params = ['address']


class HospitalDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all()
    serializer_class = s.Hospital
    lookup_field = 'uuid'
