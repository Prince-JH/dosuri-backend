from django.contrib.auth import get_user_model
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef, Count, Subquery
from django.db.models.functions import Coalesce
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
    models as m,
    serializers as s,
    filters as hf,
    pagings as hp
)
from dosuri.common import filters as f


class HospitalList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all().prefetch_related('hospital_image').annotate(
        article_count=Count('article')).annotate(
        latest_article=Subquery(
            cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                '-created_at').values('content')[:1]),
        latest_article_created_at=Subquery(
            cmm.Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                '-created_at').values('created_at')[:1])
    )
    serializer_class = s.Hospital
    filter_backends = [rf.OrderingFilter, rf.SearchFilter, hf.HospitalDistanceOrderingFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name']
    uuid_filter_params = ['hospital_address_assoc__address']
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']


class HospitalDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all().prefetch_related('hospital_keyword_assoc', 'hospital_keyword_assoc__keyword')
    serializer_class = s.HospitalDetail
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            user = get_user_model().objects.first()
        return self.queryset.annotate(
            keywords=ArraySubquery(
                m.HospitalKeywordAssoc.objects.filter(hospital=OuterRef('pk')).values_list('keyword__name', flat=True)),
            is_up=Coalesce(Subquery(
                m.HospitalUserAssoc.objects.filter(user=user, hospital=OuterRef('pk')).values('is_up')[:1]
            ), False)
        )


class HospitalCalendarList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalCalendar.objects.select_related('hospital').all()
    serializer_class = s.HospitalCalendar
    filter_backends = [f.ForeignUuidFilter]
    uuid_filter_params = ['hospital']


class HospitalCalendarDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalCalendar.objects.all()
    serializer_class = s.HospitalCalendar
    lookup_field = 'uuid'


class HospitalImageList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    pagination_class = None
    queryset = m.HospitalImage.objects.select_related('hospital').all()
    serializer_class = s.HospitalImage
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, f.ForeignUuidBodyFilter]
    ordering_field = '__all__'
    ordering = 'hospital'
    uuid_filter_params = ['hospital']
    uuid_filter_body_params = ['hospital']


class HospitalImageDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalImage.objects.all()
    serializer_class = s.HospitalImage
    lookup_field = 'uuid'


class HospitalAddressAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalAddressAssoc.objects.select_related('hospital', 'address').all()
    serializer_class = s.HospitalAddressAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital', 'address']


class HospitalAddressAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalAddressAssoc.objects.all()
    serializer_class = s.HospitalAddressAssoc
    lookup_field = 'uuid'


class DoctorList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Doctor.objects.select_related('hospital').all().prefetch_related('doctor_detail',
                                                                                  'doctor_keyword_assoc',
                                                                                  'doctor_keyword_assoc__keyword').annotate(
        keywords=ArraySubquery(
            m.DoctorKeywordAssoc.objects.filter(doctor=OuterRef('pk')).values_list('keyword__name', flat=True))
    )
    serializer_class = s.Doctor
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class DoctorDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Doctor.objects.all()
    serializer_class = s.Doctor
    lookup_field = 'uuid'


class DoctorDescriptionList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.select_related('doctor').all()
    serializer_class = s.DoctorDescription
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, f.ForeignUuidBodyFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor']
    uuid_filter_body_params = ['doctor']


class DoctorDescriptionDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    lookup_field = 'uuid'


class HospitalKeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeyword.objects.all().annotate(
        hospital=Subquery(m.HospitalKeywordAssoc.objects.filter(keyword=OuterRef('pk')).values('hospital__uuid')[:1])
    )
    pagination_class = None
    serializer_class = s.HospitalKeyword
    filter_backends = [rf.OrderingFilter, f.UuidSetBodyFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    ordering = 'hospital'
    uuid_filter_params = ['hospital_keyword_assoc__hospital']


class HospitalKeywordDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeyword.objects.all()
    serializer_class = s.HospitalKeyword
    lookup_field = 'uuid'


class DoctorKeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorKeyword.objects.all().annotate(
        doctor=Subquery(m.DoctorKeywordAssoc.objects.filter(keyword=OuterRef('pk')).values('doctor__uuid')[:1])
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
    queryset = m.DoctorKeyword.objects.all()
    serializer_class = s.DoctorKeyword
    lookup_field = 'uuid'


class HospitalKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeywordAssoc.objects.select_related('hospital', 'keyword').all()
    serializer_class = s.HospitalKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital', 'keyword']


class HospitalKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalKeywordAssoc.objects.all()
    serializer_class = s.HospitalKeywordAssoc
    lookup_field = 'uuid'


class DoctorKeywordAssocList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorKeywordAssoc.objects.select_related('doctor', 'keyword').all()
    serializer_class = s.DoctorKeywordAssoc
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor', 'keyword']


class DoctorKeywordAssocDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorKeywordAssoc.objects.all()
    serializer_class = s.DoctorKeywordAssoc
    lookup_field = 'uuid'


class HospitalTreatmentList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalTreatment.objects.select_related('hospital').all()
    serializer_class = s.HospitalTreatment
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


class HospitalTreatmentDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.HospitalTreatment.objects.all()
    serializer_class = s.HospitalTreatment
    lookup_field = 'uuid'


class HospitalUserAssoc(g.CreateAPIView):
    permission_classes = [p.IsAuthenticated]
    queryset = m.HospitalUserAssoc.objects.all()
    serializer_class = s.HospitalUserAssoc

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


'''
내 주변 TOP 병원 등, drf 오버라이드가 필요한 views
'''


class TopHospitalList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all()
    serializer_class = s.TopHospital

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data)
