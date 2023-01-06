from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p, status
)
from rest_framework.response import Response

from dosuri.user import (
    models as um,
    serializers as s,
    auth as a,
    exceptions as uexc,
)
from dosuri.common import (
    generics as cg
)


class Auth(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = s.Auth


class SuperUserAuth(g.RetrieveAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = s.Auth

    def get(self, request, *args, **kwargs):
        user = um.User.objects.get(username="dosuri")
        tokens = a.get_tokens_for_user(user)
        return Response(tokens)


class UserList(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = s.User
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserNickname(g.RetrieveAPIView):
    permission_classes = [p.AllowAny]

    @extend_schema(parameters=[
        OpenApiParameter(
            name="nickname",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ])
    def get(self, request, *args, **kwargs):
        nickname = request.GET.get('nickname')
        qs = get_user_model().objects.filter(nickname=nickname)
        if qs.exists():
            raise uexc.NicknameDuplicated()
        else:
            return Response(data={}, status=status.HTTP_200_OK)


class UserDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = s.User

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InsuranceUserAssocList(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.InsuranceUserAssoc.objects.all()
    serializer_class = s.InsuranceUserAssoc
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(insurance=um.Insurance.objects.all().first(), user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserPointHistoryList(cg.UserAuthListAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserPointHistory.objects.all()
    serializer_class = s.UserPointHistory
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class UserPointHistoryDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserPointHistory.objects.all()
    serializer_class = s.UserPointHistory


class UserTotalPoint(g.RetrieveAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = s.UserTotalPoint

    def retrieve(self, request, *args, **kwargs):
        total_point = um.UserPointHistory.objects.get_total_point(user=request.user)
        serializer = self.serializer_class(data={'total_point': total_point})
        serializer.is_valid()
        return Response(serializer.data)


class UserNotificationList(cg.UserAuthListAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserNotification.objects.all()
    serializer_class = s.UserNotification
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class UserNotificationDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserNotification.objects.all()
    serializer_class = s.UserNotification

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        um.UserNotification.objects.check_notification(instance.uuid)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
