from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from dosuri.user import views as v

urlpatterns = [

    path('v1/token/verify', TokenVerifyView.as_view(), name='token-obtain-pair'),
    path('v1/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

    path('v1/auth', v.Auth.as_view(), name='kakao-auth'),
    path('v1/users', v.UserList.as_view(), name='user'),
    path('v1/users/token', v.UserToken.as_view(), name='user'),
    path('v1/users/nickname', v.UserNickname.as_view(), name='user-nickname'),
    path('v1/auth/superuser', v.SuperUserAuth.as_view(), name='superuser-auth'),

    path('v1/users/me', v.UserDetail.as_view(), name='user-detail'),
    path('v1/users/me/point-histories', v.UserPointHistoryList.as_view(), name='user-point-history'),
    path('v1/users/me/point-histories/<uuid>', v.UserPointHistoryDetail.as_view(), name='user-point-history'),
    path('v1/users/me/point/', v.UserTotalPoint.as_view(), name='user-total-point'),
    path('v1/users/me/notifications', v.UserNotificationList.as_view(), name='user-notification'),
    path('v1/users/me/notifications/<uuid>', v.UserNotificationDetail.as_view(), name='user-notification'),

    path('v1/users/me/resign', v.UserResignHistoryList.as_view(), name='user-resign'),

    path('v1/insurance-user-assocs', v.InsuranceUserAssocList.as_view(), name='insurance-user-assoc'),
]
