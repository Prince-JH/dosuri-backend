from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)

from dosuri.common import models as cm
from dosuri.community import (
    models as m,
    serializers as s
)
from dosuri.common import filters as f




# Todo verification 로직 타기
class ReviewList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all()
    serializer_class = s.Article
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, rf.SearchFilter]
    ordering_field = '__all__'

