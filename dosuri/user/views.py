from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)
from rest_framework_simplejwt.views import TokenViewBase

from dosuri.user import (
    models as m,
    serializers as s,
    auth as a
)


class KakaoAuth(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = s.KakaoAuth
