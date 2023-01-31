from rest_framework import filters
from django.db.models import Count, Case, When
from rest_framework.settings import api_settings

from dosuri.hospital import (
    filter_schema as fsc,
    models as hm
)
from dosuri.community import (
    models as cmm,
    constants as cmc,
)
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F


class HospitalDistanceFilter(fsc.HospitalDistanceFilterSchema,
                             filters.BaseFilterBackend):
    distance_param = 'distance'
    latitude_param = 'latitude'
    longitude_param = 'longitude'

    def filter_queryset(self, request, queryset, view, now=None):
        latitude = self.get_latitude_param(request)
        longitude = self.get_longitude_param(request)
        if not latitude or not longitude:
            return queryset

        latitude, longitude = float(latitude), float(longitude)
        distance = self.get_distance_param(view)

        if not distance:
            return queryset

        latitude_range = self.get_latitude_range(latitude, distance)
        longitude_range = self.get_longitude_range(longitude, distance)
        return queryset.filter(latitude__range=latitude_range, longitude__range=longitude_range)

    def get_distance_param(self, view):
        return view.hospital_distance_range  # 현재는 서버에 정적으로 선언
        # return request.GET.get(self.distance_param, None) # 클라이언트에서 주입 받을수도 있음

    def get_latitude_param(self, request):
        return request.GET.get(self.latitude_param, None)

    def get_longitude_param(self, request):
        return request.GET.get(self.longitude_param, None)

    def get_latitude_range(self, latitude, km_distance):
        delta = round(km_distance / 111.19, 13)
        return round(latitude - delta, 13), round(latitude + delta, 13)

    def get_longitude_range(self, longitude, km_distance):
        delta = round(km_distance / 88.80, 13)
        return round(longitude - delta, 13), round(longitude + delta, 13)

    def get_distance_annotation(self, latitude, longitude):
        d_lat = (F('latitude') - latitude) * 111.19
        d_long = (F('longitude') - longitude) * 88.80

        return Sqrt((d_lat * d_lat) + (d_long * d_long))


class ReviewCountOrderingFilter(fsc.PageQueryParamFilterSchema, filters.BaseFilterBackend):
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
            extra_hospital_ids = queryset.exclude(
                id__in=cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW).all().values_list('hospital',
                                                                                                     flat=True)).order_by(
                '?')[:extra].values_list('id', flat=True)
            list_hospital_ids = list(hospital_ids[start:]) + list(extra_hospital_ids)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_hospital_ids)])
        return queryset.filter(id__in=list_hospital_ids).order_by(preserved)


class ReviewNewOrderingFilter(fsc.PageQueryParamFilterSchema, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view, now=None):
        page = int(request.GET.get('page', 1))
        page_size = api_settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size
        list_hospital_ids = list(dict.fromkeys(
            cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW).order_by('-created_at').values_list(
                'hospital', flat=True)))
        if len(list_hospital_ids) >= end:
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_hospital_ids[start: end])])
        else:
            if start > len(list_hospital_ids):
                extra = page_size
            else:
                extra = end - len(list_hospital_ids)
            extra_hospital_ids = queryset.exclude(
                id__in=cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW).all().values_list('hospital',
                                                                                                     flat=True)).order_by(
                '?')[:extra].values_list('id', flat=True)
            list_hospital_ids = list_hospital_ids[start:] + list(extra_hospital_ids)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_hospital_ids)])
        return queryset.filter(id__in=list_hospital_ids).order_by(preserved)


class DoctorPositionFilter(fsc.DoctorPositionFilterSchema, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        position = request.GET.get('position')
        if not position:
            return queryset
        return queryset.filter(position=position)


class HospitalSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        word = request.GET.get('search')
        if word:
            hm.HospitalSearch.objects.save_search(request.user, word)

        return super().filter_queryset(request, queryset, view)


class ExtraOrderingByIdFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            ordering.append('id')
        return ordering
