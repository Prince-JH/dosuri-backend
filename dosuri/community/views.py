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
from django.db.models import Count
from datetime import datetime, timedelta

class HotArticleList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.filter(created_at__gte=datetime.now()-timedelta(days=7)).annotate(comment_count=Count('article_comment')).order_by('-comment_count')[:3]
    serializer_class = s.GetArticle
    filter_backends = []
    ordering_field = '__all__'
    def list(self, request, *args, **kwargs): ## 준호님 요청에 의해 시간 표기 로직을 백엔드에서 수행, 추후 프론트에서 작업시 해당 함수 제거 요망
        response = super().list(request, *args, **kwargs)
        now = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        for item in response.data['results']:
            print(item['created_at'])
            created_at = datetime.strptime(item['created_at'], date_format)
            total_seconds = (now-created_at).total_seconds()
            if total_seconds < 60:
                item['created_at'] = str(int(total_seconds))+ '초 전'
            elif total_seconds/60 < 60:
                item['created_at'] = str(int(total_seconds/60))+ '분 전'
            elif total_seconds/3600 < 24:
                item['created_at'] = str(int(total_seconds/3600))+ '시간 전'
            elif (total_seconds/3600)/24 < 30:
                item['created_at'] = str(int((total_seconds/3600)/24))+ '일 전'
            elif ((total_seconds/3600)/24)/30 < 12:
                print(total_seconds/86400)
                item['created_at'] = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
            else:
                item['created_at'] = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return response

class ArticleList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.all().annotate(comment_count=Count('article_comment'))
    serializer_class = s.Article
    read_serializer_class = s.GetArticle
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, f.ArticleTypeFilter]
    uuid_filter_params = ['hospital']
    ordering_field = '__all__'
    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return self.read_serializer_class

        return self.serializer_class
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def list(self, request, *args, **kwargs): ## 준호님 요청에 의해 시간 표기 로직을 백엔드에서 수행, 추후 프론트에서 작업시 해당 함수 제거 요망
        response = super().list(request, *args, **kwargs)
        now = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        for item in response.data['results']:
            created_at = datetime.strptime(item['created_at'], date_format)
            total_seconds = (now-created_at).total_seconds()
            if total_seconds < 60:
                item['created_at'] = str(int(total_seconds))+ '초 전'
            elif total_seconds/60 < 60:
                item['created_at'] = str(int(total_seconds/60))+ '분 전'
            elif total_seconds/3600 < 24:
                item['created_at'] = str(int(total_seconds/3600))+ '시간 전'
            elif (total_seconds/3600)/24 < 30:
                item['created_at'] = str(int((total_seconds/3600)/24))+ '일 전'
            elif ((total_seconds/3600)/24)/30 < 12:
                print(total_seconds/86400)
                item['created_at'] = str(int(((total_seconds/3600)/24)/30))+ '개월 전'
            else:
                item['created_at'] = str(int((((total_seconds/3600)/24)/30)/12))+ '년 전'
        return response


# class CreateArticle(g.CreateAPIView):
#     permission_classes = [p.AllowAny]
#     queryset = m.Article.objects.all()
#     serializer_class = s.Article
#     filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
#     uuid_filter_params = ['hospital']
#     ordering_field = '__all__'
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

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

class ArticleDetail(g.RetrieveAPIView):
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
