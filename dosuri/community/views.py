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




class ArticleList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all()
    serializer_class = s.Article
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class ArticleAttachList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAttach.objects.all()
    serializer_class = s.ArticleAttach
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

