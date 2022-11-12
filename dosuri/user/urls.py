from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from dosuri.user import views as v

urlpatterns = [

    path('v1/token/verify/', TokenVerifyView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v1/auth/', v.Auth.as_view(), name='kakao-auth'),
    path('v1/users/', v.UserList.as_view(), name='user-list'),
    path('v1/users/<uuid>/', v.UserDetail.as_view(), name='user-detail'),
]
