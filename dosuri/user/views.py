from django.contrib.auth import get_user_model
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
    permission_classes = [p.AllowAny]
    queryset = um.InsuranceUserAssoc.objects.all()
    serializer_class = s.InsuranceUserAssoc
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'
