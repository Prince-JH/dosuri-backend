from django.contrib import admin
from django.urls import path, include

from dosuri.community import views as v

urlpatterns = [

    path('v1/community/reviews', v.ReviewList.as_view(), name='review'),

]
