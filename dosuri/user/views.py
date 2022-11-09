from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)
from dosuri.user import (
    models as m,
    serializers as s
)


class KakaoAuth(g.CreateAPIView):
    serializer_class = s.KakaoAuth
