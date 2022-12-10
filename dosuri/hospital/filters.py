from rest_framework import filters
from django.db.models import Count, Case, When
from rest_framework.settings import api_settings

from dosuri.hospital import filter_schema as fsc
from dosuri.community import (
    models as cmm,
    constants as cmc,
)


class ReviewOrderingFilter(fsc.ReviewOrderingFilter, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view, now=None):
        page = int(request.GET.get('page', 1))
        page_size = api_settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size
        hospital_ids = cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW).values_list('hospital',
                                                                                               flat=True).annotate(
            count=Count('hospital')).order_by('-count')
        if hospital_ids.count() >= end:
            list_hospital_ids = list(hospital_ids[start: end])
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list(hospital_ids)[start: end])])
        else:
            if start > hospital_ids.count():
                extra = page_size
            else:
                extra = end - hospital_ids.count()
            extra_hospital_ids = list(queryset.exclude(
                id__in=cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW).all().values_list('hospital',
                                                                                                     flat=True)).order_by(
                '?')[:extra].values_list('id', flat=True))
            list_hospital_ids = list(hospital_ids[start:]) + extra_hospital_ids
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_hospital_ids)])
        return queryset.filter(id__in=list_hospital_ids).order_by(preserved)
