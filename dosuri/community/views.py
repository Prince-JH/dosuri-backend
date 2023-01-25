from django.utils import timezone
from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p,
    status,
)

from dosuri.common import models as cm
from dosuri.hospital import models as hm
from dosuri.community import (
    models as m,
    serializers as s
)
from dosuri.common import filters as f
from rest_framework.response import Response
from django.db.models import Count

from datetime import datetime, timedelta
from django.contrib.postgres.aggregates import ArrayAgg


class HotArticleList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Article.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).annotate(
        comment_count=Count('article_comment')).order_by('-comment_count')[:3]
    serializer_class = s.GetArticle
    filter_backends = []
    ordering_fields = '__all__'


class TreatmentKeywordList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.TreatmentKeyword.objects.all()
    serializer_class = s.TreatmentKeyword
    filter_backends = []
    ordering_fields = '__all__'


class ArticleList(g.ListCreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.Article.objects.all()
    serializer_class = s.Article
    read_serializer_class = s.GetArticle
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, f.ArticleTypeFilter, f.ArticleSearchFilter]
    uuid_filter_params = ['hospital', 'user']
    ordering_fields = '__all__'

    def get_queryset(self):
        return self.queryset.prefetch_related('article_attachment_assoc',
                                              'article_attachment_assoc__attachment',
                                              'hospital') \
            .annotate(comment_count=Count('article_comment'))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.read_serializer_class

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class CreateArticle(g.CreateAPIView):
#     permission_classes = [p.AllowAny]
#     queryset = m.Article.objects.all()
#     serializer_class = s.Article
#     filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
#     uuid_filter_params = ['hospital']
#     ordering_field = '__all__'
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class ArticleDoctorAssocList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleDoctorAssoc.objects.all()
    serializer_class = s.ArticleDoctorAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_fields = '__all__'


class ArticleKeywordAssocList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleKeywordAssoc.objects.all()
    serializer_class = s.ArticleKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']
    ordering_fields = '__all__'


class ArticleDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.Article.objects.prefetch_related(
        'article_comment',
        'article_comment__article_thread').all()
    serializer_class = s.ArticleDetail
    lookup_field = 'uuid'

    def get_queryset(self):
        if self.request.method == "DELETE":
            return self.queryset.filter(user=self.request.user)
        return self.queryset


class ArticleAuth(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.ArticleAuth.objects.all()
    serializer_class = s.ArticleAuth
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    uuid_filter_params = ['article']
    ordering_fields = '__all__'


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
    serializer_class = s.PostArticleThread
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class ArticleLike(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.ArticleLike.objects.all()
    serializer_class = s.ArticleLike

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class SampleReview(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.Article.objects.all()

    def create(self, request, *args, **kwargs):
        content_list = ['정말 별로에요. 원장님이 변-태 같이 더듬는거 같아서 끔찍했고 다시는 가고 싶지 않아요.\n 트라우마만 생겨서 왔어요.',
                        '시원하고 좋았습니다. 가격도 합리적이었으며 다시 방문할 의사가 있습니다.']
        for content in content_list:
            hospital = hm.Hospital.objects.order_by('?')[0]
            article = m.Article(
                user=request.user,
                article_type='review',
                hospital=hospital,
                content=content
            )
            article.save()
            att_1 = m.ArticleAttachmentAssoc(
                article=article,
                attachment_id=31
            )
            att_2 = m.ArticleAttachmentAssoc(
                article=article,
                attachment_id=32
            )
            att_1.save()
            att_2.save()
            article_keyword = m.ArticleKeywordAssoc(
                article=article,
                treatment_keyword_id=2
            )
            article_keyword.save()
            article_detail = m.ArticleDetail(
                article=article,
                treatment_effect=3,
                doctor_kindness=3,
                therapist_kindness=3,
                staff_kindness=3,
                clean_score=3,
                cost=53500,
                treat_count=2
            )
            article_detail.save()
            article_auth = m.ArticleAuth(
                article=article,
                sensitive_agreement=True,
                personal_agreement=True
            )
            article_auth.save()
            att_3 = m.AuthAttachmentAssoc(
                article_auth=article_auth,
                attachment_id=33
            )
            att_4 = m.AuthAttachmentAssoc(
                article_auth=article_auth,
                attachment_id=36
            )
        return Response(status=status.HTTP_201_CREATED)
