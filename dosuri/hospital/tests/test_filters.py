import pytest

from dosuri.hospital import (
    models as hm,
    filters as hf
)


class DummyView:
    page = 1


class TestArticleOrderingFilter:
    @pytest.mark.django_db
    def test_hospital_queryset_order_by_article_count(
            self, rf, hospital_test_A, hospital_test_B, hospital_test_C, article_A_hospital_A, article_B_hospital_A,
            article_A_hospital_B):
        url = f'/'
        request = rf.get(url)
        queryset = hm.Hospital.objects.all().prefetch_related('article')
        assert queryset.count() == 3

        _filter = hf.ReviewOrderingFilter()
        view = DummyView()
        filtered_qs = _filter.filter_queryset(request, queryset, view)
        assert filtered_qs.count() == 3
        assert filtered_qs[0].uuid == hospital_test_A.uuid
        assert filtered_qs[1].uuid == hospital_test_B.uuid
        assert filtered_qs[2].uuid == hospital_test_C.uuid
