from django.contrib import admin
from django.urls import path, include

from dosuri.community import views as v

urlpatterns = [

    path('v1/community/articles', v.ArticleList.as_view(), name='article'),
    path('v1/community/article-attaches', v.ArticleAttachList.as_view(), name='attach'),

]
