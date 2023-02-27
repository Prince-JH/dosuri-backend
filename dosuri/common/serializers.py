from rest_framework import serializers as s
from dosuri.common import (
    models as cm,
    utils as cu
)
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes



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
    uuid: s.Field = s.CharField(required=False)
    bucket_name: s.Field = s.CharField(write_only=True, allow_null=False)
    path: s.Field = s.CharField(write_only=True, allow_null=False)
    created_at: s.Field = s.DateTimeField(read_only=True)
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = cm.Attachment
        exclude = ('id',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_signed_path(self, obj):
        return cu.generate_signed_path(obj)


class PutAttachment(s.ModelSerializer):
    uuid: s.Field = s.CharField()
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = cm.Attachment
        fields = ('uuid', 'signed_path')

    @extend_schema_field(OpenApiTypes.STR)
    def get_signed_path(self, obj):
        return cu.generate_signed_path(obj)
