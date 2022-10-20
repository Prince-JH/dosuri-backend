from rest_framework import serializers as s

from dosuri.hospital import models as m


class Hospital(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    address: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=m.Address.objects.all()
    )
    name: s.Field = s.CharField()
    introduction: s.Field = s.CharField(allow_blank=True)
    phone_no: s.Field = s.CharField(allow_blank=True)
    up_count: s.Field = s.IntegerField(read_only=True)
    view_count: s.Field = s.IntegerField(read_only=True)
    is_partner: s.Field = s.BooleanField()
    opened_at: s.Field = s.DateTimeField(allow_null=True)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = m.Hospital
        exclude = ('id',)

