from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, When
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
    constants as uc
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


class UserToken(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = s.UserToken

    def create(self, request, *args, **kwargs):
        qs = um.User.objects.filter(username=request.data.get('username'))
        if not qs.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tokens = a.get_tokens_for_user(qs.first())
        return Response(tokens)


class UserList(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = s.User
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


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
            if qs.first() == request.user:
                return Response(data={}, status=status.HTTP_200_OK)
            raise uexc.NicknameDuplicated()
        else:
            return Response(data={}, status=status.HTTP_200_OK)


class UserDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = get_user_model().objects.filter()
    serializer_class = s.User
    lookup_field = 'uuid'

    def get_object(self):
        return self.request.user


class UserNotice(g.UpdateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = get_user_model().objects.filter()
    serializer_class = s.UserNotice

    def get_object(self):
        return self.request.user


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


class UserPointHistoryList(cg.UserAuthListCreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserPointHistory.objects.all()
    serializer_class = s.UserPointHistory
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class UserPointHistoryDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserPointHistory.objects.all()
    serializer_class = s.UserPointHistory
    lookup_field = 'uuid'


class UserTotalPoint(g.RetrieveAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = s.UserTotalPoint

    def retrieve(self, request, *args, **kwargs):
        total_point = um.UserPointHistory.objects.get_total_point(user=request.user)
        serializer = self.serializer_class(data={'total_point': total_point})
        serializer.is_valid()
        return Response(serializer.data)


class UserNotificationList(cg.UserAuthListCreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserNotification.objects.all()
    serializer_class = s.UserNotification
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class UserNotificationDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserNotification.objects.all()
    serializer_class = s.UserNotification
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        um.UserNotification.objects.check_notification(instance.uuid)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserResignHistoryList(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserResignHistory.objects.all()
    serializer_class = s.UserResignHistory

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserAddressList(g.ListCreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserAddress.objects.all()
    serializer_class = s.UserAddress
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, user):
        return self.queryset.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request.user)).order_by(
            Case(
                When(address_type=uc.ADDRESS_HOME, then=0),
                When(address_type=uc.ADDRESS_OFFICE, then=1),
                default=2,
                output_field=models.IntegerField(),
            ),
            '-created_at'
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserAddressDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserAddress.objects.all()
    serializer_class = s.UserAddressDetail
    lookup_field = 'uuid'


class UserPersonalInformationAgreementList(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.UserPersonalInformationAgreement.objects.all()
    serializer_class = s.UserPersonalInformationAgreement

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
