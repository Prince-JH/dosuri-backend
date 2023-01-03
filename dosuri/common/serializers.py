from rest_framework import serializers as s
from dosuri.common import models as cm
from django.conf import settings
from drf_yasg.utils import swagger_serializer_method
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from datetime import datetime, timedelta
from urllib import parse
import rsa


private_key_path= settings.DOSURI_IMAGE_PRIVATE_KEY_PATH
key_id = settings.DOSURI_IMAGE_PUBLIC_KEY_ID
host_domain = settings.HOST_DOMAIN

def rsa_signer(message):
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

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
        try:
            url = 'http://'+obj.bucket_name + '.' + host_domain + '/' + parse.quote(obj.path)
            expire_date = datetime.now() + timedelta(days=1)

            signed_url = cloudfront_signer.generate_presigned_url(
                url, date_less_than=expire_date)
            return signed_url
        except:
            import traceback
            traceback.print_exc()
            return None
        return signed_url


class PutAttachment(s.ModelSerializer):
    uuid: s.Field = s.CharField()
    signed_path: s.Field = s.SerializerMethodField()

    class Meta:
        model = cm.Attachment
        fields = ('uuid', 'signed_path')

    @swagger_serializer_method(serializer_or_field=s.CharField)
    def get_signed_path(self, obj):
        try:
            url = 'http://'+obj.bucket_name + '.' + host_domain + '/' + obj.path
            expire_date = datetime.now() + timedelta(days=1)

            signed_url = cloudfront_signer.generate_presigned_url(
                url, date_less_than=expire_date)
            return signed_url
        except:
            import traceback
            traceback.print_exc()
            return None
        return signed_url