from rest_framework.response import Response
from rest_framework import (
    generics as g,
    filters as rf,
    permissions as p
)
from rest_framework.utils.urls import replace_query_param, remove_query_param
from django.db.models import Count, OuterRef, Subquery
from dosuri.common import models as cm
from dosuri.hospital import (
    models as m,
    serializers as s,
    filters as hf
)
from dosuri.common import filters as f
from dosuri.community import models as comm

class HospitalList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    article_query_set = comm.Article.objects.filter(hospital=OuterRef('pk')).order_by('-created_at')
    queryset = m.Hospital.objects.all().annotate(article_count=Count('article')).annotate(latest_article_content=Subquery(article_query_set.values('content')[:1]))
    serializer_class = s.Hospital
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter, rf.SearchFilter]
    ordering_field = '__all__'
    ordering = ['view_count']
    search_fields = ['name']
    uuid_filter_params = ['hospital_address_assoc__address']


class HospitalDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all()
    serializer_class = s.Hospital
    lookup_field = 'uuid'


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
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['hospital']


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
    queryset = m.Doctor.objects.select_related('hospital').all()
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
    filter_backends = [rf.OrderingFilter, f.ForeignUuidFilter]
    ordering_field = '__all__'
    uuid_filter_params = ['doctor']


class DoctorDescriptionDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.DoctorDescription.objects.all()
    serializer_class = s.DoctorDescription
    lookup_field = 'uuid'


class KeywordList(g.ListCreateAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Keyword.objects.all()
    serializer_class = s.Keyword
    filter_backends = [rf.OrderingFilter]
    ordering_field = '__all__'


class KeywordDetail(g.RetrieveUpdateDestroyAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Keyword.objects.all()
    serializer_class = s.Keyword
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


class ReviewOrderHospitalList(g.ListAPIView):
    permission_classes = [p.AllowAny]
    queryset = m.Hospital.objects.all().prefetch_related('article')
    pagination_class = None
    serializer_class = s.Hospital
    filter_backends = [hf.ReviewOrderingFilter]
    page_query_param = 'page'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=self.make_response_with_paging(serializer.data))

    def make_response_with_paging(self, data):
        res = {}
        res['count'] = len(data)
        page = int(self.request.GET.get('page', 1))
        res['next'] = self.get_next_link(page)
        res['prev'] = self.get_previous_link(page)
        res['result'] = data
        return res

    def get_next_link(self, page):
        url = self.request.build_absolute_uri()
        page_number = page + 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self, page):
        url = self.request.build_absolute_uri()
        page_number = page - 1
        if page_number == 0:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
