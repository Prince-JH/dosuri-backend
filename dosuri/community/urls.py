from django.contrib import admin
from django.urls import path, include

from dosuri.community import views as v

urlpatterns = [

    path('v1/community/articles', v.ArticleList.as_view(), name='article'),
    path('v1/community/articles/<uuid>', v.ArticleDetail.as_view(), name='article-detail'),
    path('v1/community/articles-like', v.ArticleLike.as_view(), name='article-like'),
    path('v1/community/article-comment', v.ArticleComment.as_view(), name='article-comment'),
    path('v1/community/article_thread', v.ArticleThread.as_view(), name='article-thread'),
    path('v1/community/article-auth/<uuid>', v.ArticleAuthDetail.as_view(), name='auth-update'),
    path('v1/community/hot-articles', v.HotArticleList.as_view(), name='article'),
    path('v1/community/treatment-keywords', v.TreatmentKeywordList.as_view(), name='treatment-keyword'),

]
