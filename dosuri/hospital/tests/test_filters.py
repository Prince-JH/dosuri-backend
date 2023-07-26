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

    @pytest.mark.django_db
    def test_filter_with_distance_query_param_3km(
            self, rf, hospital_test_강남, hospital_test_수원):
        latitude = 37.2762816
        longitude = 127.0433978
        url = f'/?distance_range=3&latitude={latitude}&longitude={longitude}'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 2

        _filter = hf.HospitalDistanceFilter()
        view = DummyNoneDistanceView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 1


class TestAvgPricePerHourRangeFilter:
    @pytest.mark.django_db
    def test_filter_within_0_to_100000(
            self, rf, hospital_treatments_test_A):
        url = f'/?price_range_from=0&price_range_to=100000'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 1

        _filter = hf.AvgPricePerHourRangeFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 0

    @pytest.mark.django_db
    def test_filter_within_100000_to_200000(
            self, rf, hospital_treatments_test_A):
        url = f'/?price_range_from=100000&price_range_to=200000'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 1

        _filter = hf.AvgPricePerHourRangeFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 1


class TestOpenedAtRangeFilter:
    @pytest.mark.django_db
    def test_filter_should_return_one(
            self, rf, hospital_test_강남):
        url = f'/?opened_at_range_from=2022-12-31T00:00:00%2B09:00&opened_at_range_to=2023-01-05T00:00:00%2B09:00'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 1

        _filter = hf.OpenedAtRangeFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 1

    @pytest.mark.django_db
    def test_filter_should_return_two(
            self, rf, hospital_test_강남, hospital_test_수원):
        url = f'/?opened_at_range_from=2019-12-31T00:00:00%2B09:00&opened_at_range_to=2023-01-05T00:00:00%2B09:00'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all()
        assert queryset.count() == 2

        _filter = hf.OpenedAtRangeFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 2
