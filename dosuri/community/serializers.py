from rest_framework import serializers as s

import dosuri.common.models
from dosuri.community import models as comm
from dosuri.common import models as cm
from dosuri.hospital import models as hm


class Article(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    user_id: s.Field = s.IntegerField(read_only=True)
    up_count: s.Field = s.IntegerField(default=0)
    view_count: s.Field = s.IntegerField(default=0)
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.Article
        exclude = ('id',)


class ArticleAttach(s.ModelSerializer):
    uuid: s.Field = s.CharField(read_only=True)
    article: s.Field = s.SlugRelatedField(
        slug_field='uuid',
        queryset=comm.Article.objects.all()
    )
    path: s.Field = s.CharField()
    created_at: s.Field = s.DateTimeField(read_only=True)

    class Meta:
        model = dosuri.community.models.ArticleAttach
        exclude = ('id',)

