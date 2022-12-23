from django.contrib import admin
from django.urls import path, include

from dosuri.community import views as v

urlpatterns = [

    path('v1/community/articles', v.ArticleList.as_view(), name='article'),
    # path('v1/community/articles', v.CreateArticle.as_view(), name='article'),
    path('v1/community/articles/<uuid>', v.ArticleDetail.as_view(), name='article-detail'),
    # path('v1/community/article-attaches', v.ArticleAttachList.as_view(), name='article-attach'),
    # path('v1/community/article-detail', v.ArticleDetail.as_view(), name='article-detail'),
    # path('v1/community/doctor-assoc', v.ArticleDoctorAssocList.as_view(), name='doctor'),
    # path('v1/community/article-keyword-assoc', v.ArticleKeywordAssocList.as_view(), name='treatment'),
    # path('v1/community/article-auth', v.ArticleAuth.as_view(), name='article-auth'),
    # path('v1/community/auth-attach', v.AuthAttach.as_view(), name='auth-attach'),
    path('v1/community/article-comment', v.ArticleComment.as_view(), name='article-comment'),
    path('v1/community/article_thread', v.ArticleThread.as_view(), name='article-thread'),
    path('v1/community/article-auth/<uuid>', v.ArticleAuthDetail.as_view(), name='auth-update'),

]
