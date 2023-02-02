from datetime import timedelta
from random import randint

from django.contrib.auth import get_user_model
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef, Count, Subquery, Q, F, Avg, Func
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p,
    status,
)

from dosuri.common import models as cm
from dosuri.community import (
    models as cmm,
    constants as cmc,
)
from dosuri.hospital import (
    models as hm,
    serializers as s,
    filters as hf,
    pagings as hp,
    constants as hc,
    model_mixins as hmx,
)
from dosuri.common import filters as f

class TempHospital(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE)
    serializer_class = s.PostHospital

class HospitalList(hmx.HospitalDistance, g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment').annotate_extra_fields()
    serializer_class = s.Hospital
    filter_backends = [hf.ExtraOrderingByIdFilter, rf.SearchFilter, hf.HospitalDistanceFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name']
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']
    hospital_distance_range = None


class HospitalAddressFilteredList(hmx.HospitalDistance, g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment').annotate_extra_fields()
    serializer_class = s.Hospital
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        address_filtered_qs = queryset.get_address_filtered_queryset(request.user)
        ordered_qs = self.filter_queryset(address_filtered_qs)

        page = self.paginate_queryset(ordered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ordered_qs, many=True)
        return Response(serializer.data)


class HospitalCurrentAddressFilteredList(hmx.HospitalDistance, g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment').annotate_extra_fields()
    serializer_class = s.Hospital
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalDistanceFilter]
    ordering_field = '__all__'
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']
    hospital_distance_range = 5


class HospitalCurrentAddressFilteredAvgPriceList(hmx.HospitalDistance, g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment').annotate_extra_fields().annotate_avg_price_per_hour()
    serializer_class = s.GoodPriceHospital
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalDistanceFilter]
    ordering_field = '__all__'
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']
    hospital_distance_range = 5


class HospitalDetail(g.CreateAPIView, g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_keyword_assoc',
                                                                                      'hospital_keyword_assoc__keyword',
                                                                                      'hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment')
    serializer_class = s.HospitalDetail
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            user = get_user_model().objects.first()
        return self.queryset.annotate(
            keywords=ArraySubquery(
                hm.HospitalKeywordAssoc.objects.filter(hospital=OuterRef('pk')).values_list('keyword__name',
                                                                                            flat=True)),
            is_up=Coalesce(Subquery(
                hm.HospitalUserAssoc.objects.filter(user=user, hospital=OuterRef('pk')).values('is_up')[:1]
            ), False)
        )

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increase_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HospitalCalendarList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalCalendar.objects.select_related('hospital').all()
    serializer_class = s.HospitalCalendar
    filter_backends = [f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']


class HospitalCalendarDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalCalendar.objects.all()
    serializer_class = s.HospitalCalendar
    lookup_field = 'uuid'


class HospitalAddressAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalAddressAssoc.objects.select_related('hospital', 'address').all()
    serializer_class = s.HospitalAddressAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital', 'address']


class HospitalAddressAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalAddressAssoc.objects.all()
    serializer_class = s.HospitalAddressAssoc
    lookup_field = 'uuid'


class DoctorList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Doctor.objects.select_related('hospital').all().prefetch_related('doctor_detail',
                                                                                   'doctor_keyword_assoc',
                                                                                   'doctor_keyword_assoc__keyword',
                                                                                   'doctor_attachment_assoc',
                                                                                   'doctor_attachment_assoc__attachment').annotate(
        keywords=ArraySubquery(
            hm.DoctorKeywordAssoc.objects.filter(doctor=OuterRef('pk')).values_list('keyword__name', flat=True))
    )
    serializer_class = s.Doctor
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, hf.DoctorPositionFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class DoctorDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Doctor.objects.all().prefetch_related('doctor_attachment_assoc')
    serializer_class = s.Doctor
    lookup_field = 'uuid'


class DoctorDescriptionList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorDescription.objects.select_related('doctor').all()
    serializer_class = s.DoctorDescription
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, f.ForeignUuidBodyFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor']
    uuid_filter_body_params = ['doctor']


class DoctorDescriptionDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    lookup_field = 'uuid'


class HospitalKeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalKeyword.objects.all().annotate(
        hospital=Subquery(hm.HospitalKeywordAssoc.objects.filter(keyword=OuterRef('pk')).values('hospital__uuid')[:1])
    )
    pagination_class = None
    serializer_class = s.HospitalKeyword
    filter_backends = [rf.OrderingFilter, f.UuidSetBodyFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    ordering = 'hospital'
    uuid_filter_params = ['hospital_keyword_assoc__hospital']


class HospitalKeywordDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalKeyword.objects.all()
    serializer_class = s.HospitalKeyword
    lookup_field = 'uuid'


class DoctorKeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorKeyword.objects.all().annotate(
        doctor=Subquery(hm.DoctorKeywordAssoc.objects.filter(keyword=OuterRef('pk')).values('doctor__uuid')[:1])
    )
    pagination_class = None
    serializer_class = s.DoctorKeyword
    filter_backends = [rf.OrderingFilter, f.UuidSetBodyFilter, f.ForeignUuidFilter, f.ForeignUuidBodyFilter]
    ordering_field = '__all__'
    ordering = 'doctor'
    uuid_filter_params = ['doctor_keyword_assoc__doctor']
    uuid_filter_body_params = ['doctor_keyword_assoc__doctor']


class DoctorKeywordDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorKeyword.objects.all()
    serializer_class = s.DoctorKeyword
    lookup_field = 'uuid'


class HospitalKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalKeywordAssoc.objects.select_related('hospital', 'keyword').all()
    serializer_class = s.HospitalKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital', 'keyword']


class HospitalKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalKeywordAssoc.objects.all()
    serializer_class = s.HospitalKeywordAssoc
    lookup_field = 'uuid'


class DoctorKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorKeywordAssoc.objects.select_related('doctor', 'keyword').all()
    serializer_class = s.DoctorKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor', 'keyword']


class DoctorKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.DoctorKeywordAssoc.objects.all()
    serializer_class = s.DoctorKeywordAssoc
    lookup_field = 'uuid'


class HospitalTreatmentList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalTreatment.objects.select_related('hospital').all()
    serializer_class = s.HospitalTreatment
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    ordering = ['price', 'price_per_hour', 'name']
    uuid_filter_params = ['hospital']

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        res.data['price_per_hour'] = self.get_avg_price_per_hour(res.data['results'])
        return res

    def get_avg_price_per_hour(self, results):
        prices = []
        for result in results:
            price = result['price_per_hour']
            if price:
                prices.append(price)
        return sum(prices) / len(prices) if len(prices) > 0 else None


class HospitalTreatmentDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalTreatment.objects.all()
    serializer_class = s.HospitalTreatment
    lookup_field = 'uuid'


class HospitalUserAssoc(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = hm.HospitalUserAssoc.objects.all()
    serializer_class = s.HospitalUserAssoc

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HomeHospitalList(g.ListAPIView):
    pagination_class = None
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).all()
    serializer_class = s.HomeHospital

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related('hospital_attachment_assoc',
                                                                              'hospital_attachment_assoc__attachment')

        address_filtered_queryset = queryset.get_address_filtered_queryset(request.user)

        top_hospital_queryset = self.get_top_hospital_queryset(address_filtered_queryset)
        top_hospital_serializer = s.AroundHospital(top_hospital_queryset, many=True)

        new_hospital_queryset = self.get_new_hospital_queryset(address_filtered_queryset)
        new_hospital_serializer = s.AroundHospital(new_hospital_queryset, many=True)

        good_price_hospital_queryset = self.get_good_price_hospital_queryset(address_filtered_queryset)
        good_price_hospital_serializer = s.GoodPriceHospital(good_price_hospital_queryset, many=True)

        # good_review_hospital_queryset = self.get_good_review_hospital_queryset(address_filtered_queryset)
        # good_review_hospital_serializer = s.AroundHospital(good_review_hospital_queryset, many=True)

        serializer = self.get_serializer({'top_hospitals': top_hospital_serializer.data,
                                          'new_hospitals': new_hospital_serializer.data,
                                          'good_price_hospitals': good_price_hospital_serializer.data})
        return Response(serializer.data)

    def get_top_hospital_queryset(self, queryset):
        queryset = queryset.annotate_extra_fields()
        return queryset.annotate(top_count=F('up_count') + F('article_count')).order_by('-top_count')[:3]

    def get_new_hospital_queryset(self, queryset, showing_number=3):
        now = timezone.now()
        qs = queryset.filter(opened_at__gte=(now - timedelta(days=90)))
        count = qs.count()
        ids = list(qs.values_list('id', flat=True))
        if count < 3:
            extra_qs = hm.Hospital.objects.filter(opened_at__gte=(now - timedelta(days=90)),
                                                  hospital_address_assoc__address__large_area__in=['서울특별시',
                                                                                                   '경기도']).distinct()
            if count + extra_qs.count() < 3:
                extra_qs = hm.Hospital.objects.filter(opened_at__gte=(now - timedelta(days=90)))
            ids = list(set(ids + list(extra_qs.values_list('id', flat=True))))
        rand_ids = self.get_rand_ids(ids)
        return hm.Hospital.objects.filter(id__in=rand_ids).annotate_extra_fields()

    def get_good_price_hospital_queryset(self, queryset, showing_number=3):
        sub_qs = hm.HospitalTreatment.objects.filter(hospital=OuterRef('pk')).annotate(
            avg_price_per_hour=Func(F('price_per_hour'), function='AVG')).values('avg_price_per_hour').order_by(
            'avg_price_per_hour')

        qs = queryset.filter(hospital_treatment__isnull=False).distinct().annotate(
            avg_price_per_hour=Subquery(sub_qs)).filter(avg_price_per_hour__isnull=False).order_by('avg_price_per_hour')

        count = qs.count()
        if count == 0:
            return queryset.none()

        if count * 0.5 >= showing_number:
            count = int(count * 0.5)
        elif count >= showing_number:
            count = showing_number
        avg_price_per_hour = qs[count - 1].avg_price_per_hour
        if not avg_price_per_hour:
            return qs.none()

        ids = qs.filter(avg_price_per_hour__lte=avg_price_per_hour).values_list('id', flat=True)
        rand_ids = self.get_rand_ids(ids)
        return qs.annotate_extra_fields().filter(id__in=rand_ids)

    def get_good_review_hospital_queryset(self, queryset):
        count = queryset.count()
        if count == 0:
            return queryset.none()
        elif count // 2 >= 3:
            count //= 2
        qs = queryset.annotate_article_count()
        article_count = qs[count - 1].article_count
        ids = qs.filter(article_count__gte=article_count).values_list('id', flat=True)
        rand_ids = self.get_rand_ids(ids)
        return qs.annotate_extra_fields().filter(id__in=rand_ids)

    def get_rand_ids(self, ids):
        if len(ids) < 3:
            return list(ids)
        indexes = []
        while len(indexes) < 3:
            index = randint(0, len(ids) - 1)
            if index not in indexes:
                indexes.append(index)
        return [ids[index] for index in indexes]


class HospitalSearch(g.ListCreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = hm.HospitalSearch.objects.all()
    serializer_class = s.HospitalSearch
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def get_queryset(self, user):
        return self.queryset.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset(request.user)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HospitalSearchDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalSearch.objects.all()
    serializer_class = s.HospitalSearch
    lookup_field = 'uuid'
