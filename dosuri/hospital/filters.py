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
from dosuri.common import geocoding as cg
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F


class HospitalDistanceFilter(fsc.HospitalDistanceFilterSchema,
                             filters.BaseFilterBackend):
    distance_param = 'distance'
    latitude_param = 'latitude'
    longitude_param = 'longitude'

    def filter_queryset(self, request, queryset, view, now=None, **kwargs):
        latitude = kwargs.get('latitude') or getattr(view, 'latitude', None)
        longitude = kwargs.get('longitude') or getattr(view, 'longitude', None)
        if not latitude or not longitude:
            return queryset

        distance = kwargs.get('distance') or self.get_distance_param(view)

        if not distance:
            return queryset

        latitude_range = self.get_latitude_range(latitude, distance)
        longitude_range = self.get_longitude_range(longitude, distance)
        return queryset.filter(latitude__range=latitude_range, longitude__range=longitude_range)

    def get_distance_param(self, view):
        return view.hospital_distance_range  # 현재는 서버에 정적으로 선언
        # return request.GET.get(self.distance_param, None) # 클라이언트에서 주입 받을수도 있음=

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
        query = request.GET.get('search')
        if query and query[-1] == '역':
            client = cg.KaKaoGeoClient()
            coordinates = client.get_coordinates('station', query)
            if not coordinates:
                return queryset.none()
            return HospitalDistanceFilter().filter_queryset(request, queryset, view, latitude=coordinates[0],
                                                            longitude=coordinates[1], distance=1)
        else:
            return super().filter_queryset(request, queryset, view)


class ExtraOrderingByIdFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            ordering.append('id')
        return ordering


class AvgPricePerHourRangeFilter(fsc.AvgPricePerHourRangeFilterSchema, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        price_range_from = request.GET.get('price_range_from')
        price_range_to = request.GET.get('price_range_to')
        if not (price_range_from or price_range_to):
            return queryset
        qs_with_avg_price_per_hour = queryset.get_queryset_with_avg_price_per_hour()

        return qs_with_avg_price_per_hour.filter(avg_price_per_hour__range=(price_range_from, price_range_to))


class OpenedAtRangeFilter(fsc.OpenedAtRangeFilterSchema, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        opened_at_range_from = request.GET.get('opened_at_range_from')
        opened_at_range_to = request.GET.get('opened_at_range_to')
        if not (opened_at_range_from or opened_at_range_to):
            return queryset

        return queryset.filter(opened_at__range=(opened_at_range_from, opened_at_range_to))
