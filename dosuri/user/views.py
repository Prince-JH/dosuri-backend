from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)
from rest_framework.response import Response

from dosuri.user import (
    models as um,
    serializers as s,
    auth as a
)


class Auth(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = s.Auth


class UserList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = um.User.objects.all()
    serializer_class = s.User
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class UserDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = um.User.objects.all()
    serializer_class = s.User

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
