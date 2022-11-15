from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.common import (
    models as cm,
    serializers as cs
)


class AddressDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Address.objects.all()
    serializer_class = cs.Address
    lookup_field = 'uuid'
