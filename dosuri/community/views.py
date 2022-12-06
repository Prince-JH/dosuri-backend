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

class DoctorAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorAssoc.objects.all()
    serializer_class = s.DoctorAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class HospitalTreatmentAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalTreatmentAssoc.objects.all()
    serializer_class = s.HospitalTreatmentAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class ArticleDetail(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleDetail.objects.all()
    serializer_class = s.ArticleDetail
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article']
    ordering_field = '__all__'

class ArticleAuth(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAuth.objects.all()
    serializer_class = s.ArticleAuth
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article']
    ordering_field = '__all__'

class AuthAttach(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.AuthAttach.objects.all()
    serializer_class = s.AuthAttach
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article_auth']
    ordering_field = '__all__'

class ArticleUpdate(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all()
    serializer_class = s.ArticleUpdate
    lookup_field = 'uuid'