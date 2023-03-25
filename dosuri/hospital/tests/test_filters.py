import pytest

from dosuri.hospital import (
    models as hm,
    filters as hf
)
from dosuri.community import (
    models as cmm
)
from dosuri.common import (
    filters as cf
)


class DummyView:
    page = 1
    uuid_filter_body_params = ['hospital']


class Dummy1kmDistanceView:
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']
    hospital_distance_range = 1
    latitude = 37.2762816
    longitude = 127.0433978


class DummyNoneDistanceView:
    hospital_distance_filter_params = ['distance', 'latitude', 'longitude']
    hospital_distance_range = None
    latitude = 37.2762816
    longitude = 127.0433978


class TestReviewCountOrderingFilter:
    @pytest.mark.django_db
    def test_hospital_queryset_order_by_article_count(
            self, rf, hospital_test_강남, hospital_test_수원, hospital_test_C, article_A_hospital_A, article_B_hospital_A,
            article_A_hospital_B):
        url = f'/'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all().prefetch_related('article')
        assert queryset.count() == 3

        _filter = hf.ReviewCountOrderingFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 3
        assert filtered_qs[0].uuid == hospital_test_강남.uuid
        assert filtered_qs[1].uuid == hospital_test_수원.uuid
        assert filtered_qs[2].uuid == hospital_test_C.uuid


class TestReviewNewOrderingFilter:
    @pytest.mark.django_db
    def test_hospital_queryset_order_by_newer_article(
            self, rf, hospital_test_강남, hospital_test_수원, hospital_test_C, article_A_hospital_A, article_B_hospital_A,
            article_A_hospital_B
    ):
        url = f'/'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all().prefetch_related('article')
        assert queryset.count() == 3

        _filter = hf.ReviewNewOrderingFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 3
        assert filtered_qs[0].uuid == hospital_test_수원.uuid
        assert filtered_qs[1].uuid == hospital_test_강남.uuid
        assert filtered_qs[2].uuid == hospital_test_C.uuid


class TestHospitalDistanceFilter:
    @pytest.mark.django_db
    def test_filter_within_1km(
            self, rf, hospital_lat100_long100):
        url = f'/'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 1

        _filter = hf.HospitalDistanceFilter()
        view = Dummy1kmDistanceView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 0

    @pytest.mark.django_db
    def test_filter_within_infinite(
            self, rf, hospital_lat100_long100):
        url = f'/'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 1

        _filter = hf.HospitalDistanceFilter()
        view = DummyNoneDistanceView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 1
