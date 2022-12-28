from rest_framework import serializers as s

from dosuri.common import models as cm


class ReadWriteSerializerMethodField(s.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(s.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class Address(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    large_area: s.Field = s.CharField(allow_null=True)
    small_area: s.Field = s.CharField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = cm.Address
        exclude = ('id',)

class Attachment(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    bucket_name: s.Field = s.CharField(allow_null=False)
    path: s.Field = s.CharField(allow_null=False)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = cm.Attachment
        exclude = ('id','ref_uuid')
