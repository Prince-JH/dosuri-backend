from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef, Count, Subquery, Q, F, Avg, Func, Window
from django.db.models.functions import Coalesce, RowNumber, DenseRank
from django.shortcuts import get_object_or_404
from urllib.parse import quote
from rest_framework.response import Response
from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p,
    status,
)

from dosuri.common import (
    geocoding as cg
)
from dosuri.hospital import (
    models as hm,
    serializers as s,
    filters as hf,
    constants as hc,
    view_mixins as hmx,
)
from dosuri.common import filters as f


class TempHospital(g.CreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE)
    serializer_class = s.PostHospital


class HospitalList(hmx.HospitalCoordinates, g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).prefetch_related('hospital_attachment_assoc',
                                                                                      'hospital_attachment_assoc__attachment').annotate_article_related_fields()
    serializer_class = s.Hospital
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalSearchFilter, hf.HospitalDistanceFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name', 'area']
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = None


class HospitalNameList(hmx.HospitalCoordinates, g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.all()
    serializer_class = s.HospitalName
    filter_backends = [rf.SearchFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name']


class HospitalAddressFilteredList(hmx.HospitalCoordinates, g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE) \
        .prefetch_related('hospital_attachment_assoc', 'hospital_attachment_assoc__attachment') \
        .annotate_article_related_fields()
    serializer_class = s.Hospital
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalDistanceFilter]
    ordering_field = '__all__'
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = 2


class HospitalAddressFilteredAvgPriceList(hmx.HospitalCoordinates, g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE) \
        .prefetch_related('hospital_attachment_assoc', 'hospital_attachment_assoc__attachment') \
        .annotate_article_related_fields() \
        .annotate_avg_price_per_hour() \
        .filter_has_avg_price_per_hour()
    serializer_class = s.HospitalWithPrice
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalDistanceFilter, hf.AvgPricePerHourRangeFilter,
                       hf.OpenedAtRangeFilter]
    ordering_field = '__all__'
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = 2

    def get(self, request, *args, **kwargs):
        response = super().get(request, args, kwargs)
        if not request.COOKIES.get('location') and isinstance(self.request.user, AnonymousUser):
            response.set_cookie('location', quote(self.address), samesite='None', secure=True)
        return response


class HospitalMapList(hmx.HospitalCoordinates, g.ListAPIView):
    permission_classes = [p.AllowAny]
    pagination_class = None
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE) \
        .prefetch_related('hospital_attachment_assoc', 'hospital_attachment_assoc__attachment') \
        .annotate_article_related_fields() \
        .annotate_avg_price_per_hour()
    serializer_class = s.HospitalWithPriceCoordinates
    filter_backends = [hf.ExtraOrderingByIdFilter, hf.HospitalDistanceFilter, hf.AvgPricePerHourRangeFilter,
                       hf.OpenedAtRangeFilter, hf.MapTypeFilter]
    ordering_field = '__all__'
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = 2


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
        res.data['hospital_rank'] = self.get_hospital_rank(request)
        return res

    def get_avg_price_per_hour(self, results):
        prices = []
        for result in results:
            price = result['price_per_hour']
            if price:
                prices.append(price)
        return sum(prices) / len(prices) if len(prices) > 0 else None

    def get_hospital_rank(self, request):
        uuid = request.GET.get('hospital')
        if not uuid:
            return None
        try:
            hospital = hm.Hospital.objects.get(uuid=uuid)
            if not hospital.is_partner:
                return None
            client = cg.KaKaoGeoClient()
            station = hospital.near_site
            coordinates = client.get_coordinates('station', station)
            latitude = coordinates[0]
            longitude = coordinates[1]
            distance_range = 2
            latitude_range = cg.get_latitude_range(latitude, distance_range)
            longitude_range = cg.get_longitude_range(longitude, distance_range)
            hospital_with_avg_price_per_hour = hm.Hospital.objects.filter(latitude__range=latitude_range,
                                                                          longitude__range=longitude_range) \
                .annotate_avg_price_per_hour().filter_has_avg_price_per_hour().order_by('avg_price_per_hour')
            count = 1
            for hospital in hospital_with_avg_price_per_hour:
                if hospital.uuid == uuid:
                    rank = count
                count += 1

            return {'near_site': station, 'near_site_latitude': latitude, 'near_site_longitude': longitude,
                    'rank': rank, 'total_count': hospital_with_avg_price_per_hour.count(),
                    'avg_price_per_hour':
                        hospital_with_avg_price_per_hour.aggregate(total_avg_price_per_hour=Avg('avg_price_per_hour'))[
                            'total_avg_price_per_hour']}
        except hm.Hospital.objects.model.DoesNotExist:
            return None


class HospitalTreatmentDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = hm.HospitalTreatment.objects.all()
    serializer_class = s.HospitalTreatment
    lookup_field = 'uuid'


class HospitalUserAssoc(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = hm.HospitalUserAssoc.objects.all()
    serializer_class = s.HospitalUserAssoc

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ManyReviewHospitalList(hmx.HospitalCoordinates, g.ListAPIView):
    pagination_class = None
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).all()
    serializer_class = s.AroundHospital
    filter_backends = [hf.HospitalDistanceFilter]
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = 2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related('hospital_attachment_assoc',
                                                                              'hospital_attachment_assoc__attachment')

        many_review_hospital_list = queryset.get_many_review_hospital_queryset()
        serializer = self.get_serializer(many_review_hospital_list, many=True)
        return Response(serializer.data)


class HomeHospitalList(hmx.HospitalCoordinates, g.ListAPIView):
    pagination_class = None
    permission_classes = [p.AllowAny]
    queryset = hm.Hospital.objects.filter(status=hc.HOSPITAL_ACTIVE).all()
    serializer_class = s.HomeHospital
    filter_backends = [hf.HospitalDistanceFilter]
    hospital_distance_filter_params = ['distance_range', 'latitude', 'longitude']
    hospital_distance_range = 2

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related('hospital_attachment_assoc',
                                                                              'hospital_attachment_assoc__attachment')
        ad_hospital_queryset = queryset.get_ad_hospital_queryset(self.latitude, self.longitude,
                                                                 self.hospital_distance_range)
        # top_hospital_queryset = queryset.get_good_review_hospital_queryset(3 - ad_hospital_queryset.count())
        top_hospital_serializer = s.AroundHospital(ad_hospital_queryset, many=True)

        new_hospital_queryset = queryset.get_new_hospital_queryset()
        new_hospital_serializer = s.AroundHospital(new_hospital_queryset, many=True)

        good_price_hospital_queryset = queryset.get_good_price_hospital_queryset()
        good_price_hospital_serializer = s.HospitalWithPrice(good_price_hospital_queryset, many=True)

        many_review_hospital_queryset = queryset.get_many_review_hospital_queryset()
        many_review_hospital_serializer = s.AroundHospital(many_review_hospital_queryset, many=True)

        new_review_hospital_queryset = queryset.get_new_review_hospital_queryset()
        new_review_hospital_serializer = s.AroundHospital(new_review_hospital_queryset, many=True)

        serializer = self.get_serializer({'address': self.address,
                                          'top_hospitals': top_hospital_serializer.data,
                                          'new_hospitals': new_hospital_serializer.data,
                                          'good_price_hospitals': good_price_hospital_serializer.data,
                                          'many_review_hospitals': many_review_hospital_serializer.data,
                                          'new_review_hospitals': new_review_hospital_serializer.data})
        return Response(serializer.data)


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


class HospitalReservation(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = hm.HospitalReservation.objects.all()
    serializer_class = s.HospitalReservation

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HospitalContactPointList(g.ListAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = hm.HospitalContactPoint.objects.all()
    serializer_class = s.HospitalContactPoint

    def get_queryset(self):
        hospital_uuid = self.kwargs['uuid']
        hospital = get_object_or_404(hm.Hospital, uuid=hospital_uuid)
        return self.queryset.filter(hospital=hospital)
