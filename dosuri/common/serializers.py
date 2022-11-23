from rest_framework import serializers as s

from dosuri.common import models as cm


class Address(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    do: s.Field = s.CharField(allow_null=True)
    city: s.Field = s.CharField(allow_null=True)
    gun: s.Field = s.CharField(allow_null=True)
    gu: s.Field = s.CharField(allow_null=True)
    street: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = cm.Address
        exclude = ('id',)
