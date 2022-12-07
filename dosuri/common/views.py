from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.common import (
    models as cm,
    serializers as cs,
    filters as cf
)


class AddressList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Address.objects.all()
    serializer_class = cs.Address
    filter_backends = [cf.ForeignUuidFilter, cf.UuidSetFilter]
    uuid_filter_params = ['hospital_address_assoc__hospital']


class AddressDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Address.objects.all()
    serializer_class = cs.Address
    lookup_field = 'uuid'
