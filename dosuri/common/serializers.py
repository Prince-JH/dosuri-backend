from rest_framework import serializers as s
import boto3
from dosuri.common import models as cm
from django.conf import settings
from drf_yasg.utils import swagger_serializer_method

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
    bucket_name: s.Field = s.CharField(write_only=True, allow_null=False)
    path: s.Field = s.CharField(write_only=True, allow_null=False)
    created_at: s.Field = s.DateTimeField(read_only=True)
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = cm.Attachment
        exclude = ('id',)

    @swagger_serializer_method(serializer_or_field=s.CharField)
    def get_signed_path(self, obj):
        s3_client = boto3.client(
            's3', config=getattr(settings, 'AWS_CONFIG', None),
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': obj.bucket_name,
                                                            'Key': obj.path},
                                                    ExpiresIn=3600)
            return response
        except ClientError as e:
            logging.error(e)
            return None
        return response

class PutAttachment(s.ModelSerializer):
    uuid: s.Field = s.CharField()
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = cm.Attachment
        fields = ('uuid','signed_path')
    
    @swagger_serializer_method(serializer_or_field=s.CharField)
    def get_signed_path(self, obj):
        s3_client = boto3.client(
            's3', config=getattr(settings, 'AWS_CONFIG', None),
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': obj.bucket_name,
                                                            'Key': obj.path},
                                                    ExpiresIn=3600)
            return response
        except ClientError as e:
            logging.error(e)
            return None
        return response
        
