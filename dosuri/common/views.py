from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p,
    status,
)


from dosuri.common import (
    models as cm,
    serializers as cs,
    filters as cf
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def rotation_review_view(request):
    from dosuri.common.tasks import article_relocation_every_day
    from rest_framework.response import Response
    try:
        if request.headers['access-key'] == "reloc":
            article_relocation_every_day()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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


class Attachment(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Attachment.objects.all()
    serializer_class = cs.Attachment


class AttachmentDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = cm.Attachment.objects.all()
    serializer_class = cs.Attachment
    lookup_field = 'uuid'
