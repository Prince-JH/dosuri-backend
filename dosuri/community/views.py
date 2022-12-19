from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p,
    status,
)

from dosuri.common import models as cm
from dosuri.community import (
    models as m,
    serializers as s
)
from dosuri.common import filters as f
from rest_framework.response import Response




class ArticleList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all()
    serializer_class = s.Article
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleAttachList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAttach.objects.all()
    serializer_class = s.ArticleAttach
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class ArticleDoctorAssocList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleDoctorAssoc.objects.all()
    serializer_class = s.ArticleDoctorAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class ArticleKeywordAssocList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleKeywordAssoc.objects.all()
    serializer_class = s.ArticleKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'

class ArticleDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all()
    serializer_class = s.ArticleDetail
    lookup_field = 'uuid'

class ArticleAuth(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAuth.objects.all()
    serializer_class = s.ArticleAuth
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article']
    ordering_field = '__all__'

class AuthAttach(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.AuthAttach.objects.all()
    serializer_class = s.AuthAttach
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article_auth']
    ordering_field = '__all__'

class ArticleAuthDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAuth.objects.all()
    serializer_class = s.ArticleAuth
    lookup_field = 'uuid'

class ArticleComment(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.ArticleComment.objects.all()
    serializer_class = s.ArticleComment
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class ArticleThread(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.ArticleThread.objects.all()
    serializer_class = s.ArticleThread
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
