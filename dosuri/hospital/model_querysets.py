from datetime import date, timedelta
from random import randint

from django.db.models import QuerySet, Count, Subquery, OuterRef, Func, F
from django.db.models.functions import Coalesce, Sqrt
from django.utils import timezone

from dosuri.common import models as cm
from dosuri.community import constants as cmc
from dosuri.hospital import models as hm
from django.apps import apps


def get_rand_ids(ids):
    if len(ids) < 3:
        return list(ids)
    indexes = []
    while len(indexes) < 3:
        index = randint(0, len(ids) - 1)
        if index not in indexes:
            indexes.append(index)
    return [ids[index] for index in indexes]


class HospitalQuerySet(QuerySet):
    def annotate_article_related_fields(self):
        HospitalUserAssoc = apps.get_model('dosuri', 'HospitalUserAssoc')
        Article = apps.get_model('dosuri', 'Article')
        return self.annotate(
            article_count=Coalesce(Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).values(
                    'hospital').annotate(count=Count('pk')).values('count')[:1]), 0),
            up_count=Coalesce(Subquery(
                HospitalUserAssoc.objects.filter(is_up=True, hospital=OuterRef('pk')).values('hospital').annotate(
                    count=Count('pk')).values('count')[:1]), 0),
            latest_article=Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                    '-created_at').values('content')[:1]),
            latest_article_created_at=Coalesce(Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                    '-created_at').values('created_at')[:1]), date.min)
        )

    def annotate_article_count(self):
        Article = apps.get_model('dosuri', 'Article')
        return self.annotate(
            article_count=Coalesce(Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).values(
                    'hospital').annotate(count=Count('pk')).values('count')[:1]), 0))

    def annotate_up_count(self):
        HospitalUserAssoc = apps.get_model('dosuri', 'HospitalUserAssoc')
        return self.annotate(
            up_count=Coalesce(Subquery(
                HospitalUserAssoc.objects.filter(is_up=True, hospital=OuterRef('pk')).values('hospital').annotate(
                    count=Count('pk')).values('count')[:1]), 0)
        )

    def annotate_latest_article(self):
        Article = apps.get_model('dosuri', 'Article')
        self.annotate(
            latest_article=Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                    '-created_at').values('content')[:1])
        )

    def annotate_latest_article_created_at(self):
        Article = apps.get_model('dosuri', 'Article')
        self.annotate(
            Subquery(
                Article.objects.filter(article_type=cmc.ARTICLE_REVIEW, hospital=OuterRef('pk')).order_by(
                    '-created_at').values('created_at')[:1])
        )

    def get_address_filtered_queryset(self, user):
        if user.is_authenticated:
            user_addr_qs = cm.Address.objects.filter(address_user_assoc__user=user)
            if user_addr_qs.exists():
                return self.filter(hospital_address_assoc__address=user_addr_qs.first())

        return self.get_default_address_filtered_qs()

    def get_default_address_filtered_qs(self):
        return self.filter(hospital_address_assoc__address__large_area='서울특별시',
                           hospital_address_assoc__address__small_area__in=['송파구', '서초구', '강남구']).distinct()

    def annotate_avg_price_per_hour(self):
        sub_qs = hm.HospitalTreatment.objects.filter(hospital=OuterRef('pk')).annotate(
            avg_price_per_hour=Func(F('price_per_hour'), function='AVG')).values('avg_price_per_hour').order_by(
            'avg_price_per_hour')
        return self.annotate(avg_price_per_hour=Subquery(sub_qs))

    def filter_has_avg_price_per_hour(self):
        return self.filter(avg_price_per_hour__isnull=False)

    def annotate_distance(self, latitude, longitude):
        d_lat = (F('latitude') - latitude) * 111.19
        d_long = (F('longitude') - longitude) * 88.80
        return self.annotate(distance=Sqrt((d_lat * d_lat) + (d_long * d_long)))

    def get_top_hospital_queryset(self):
        return self.annotate_article_related_fields().annotate(top_count=F('up_count') + F('article_count')).order_by(
            '-top_count')[:3]

    def get_new_hospital_queryset(self, showing_number=3):
        now = timezone.now()
        qs = self.filter(opened_at__gte=(now - timedelta(days=730)))
        count = qs.count()
        ids = list(qs.values_list('id', flat=True))
        if count >= showing_number:
            ids = get_rand_ids(ids)
        return self.filter(id__in=ids).annotate_article_related_fields()

    def get_good_review_hospital_queryset(self, showing_number=3):
        count = self.count()
        if count == 0:
            return self.none()
        elif count // 2 >= showing_number:
            count //= 2
        qs = self.annotate_article_count().order_by('article_count')
        article_count = qs[count - 1].article_count
        ids = qs.filter(article_count__gte=article_count).values_list('id', flat=True)
        rand_ids = get_rand_ids(ids)
        return qs.annotate_article_related_fields().filter(id__in=rand_ids)

    def get_many_review_hospital_queryset(self, showing_number=3):
        count = self.count()
        if count == 0:
            return self.none()
        elif count // 2 >= showing_number:
            count //= 2
        qs = self.annotate_article_count().order_by('article_count')
        article_count = qs[count - 1].article_count
        ids = qs.filter(article_count__gte=article_count).values_list('id', flat=True)
        rand_ids = get_rand_ids(ids)
        return qs.annotate_article_related_fields().filter(id__in=rand_ids)

    def get_queryset_with_avg_price_per_hour(self):
        sub_qs = hm.HospitalTreatment.objects.filter(hospital=OuterRef('pk')).annotate(
            avg_price_per_hour=Func(F('price_per_hour'), function='AVG')).values('avg_price_per_hour').order_by(
            'avg_price_per_hour')

        qs = self.filter(hospital_treatment__isnull=False).distinct().annotate(
            avg_price_per_hour=Subquery(sub_qs)).filter(avg_price_per_hour__isnull=False)
        return qs

    def get_good_price_hospital_queryset(self, showing_number=3):
        qs = self.get_queryset_with_avg_price_per_hour()
        count = qs.count()
        if count == 0:
            return self.none()

        if count * 0.5 >= showing_number:
            count = int(count * 0.5)
        elif count >= showing_number:
            count = showing_number
        avg_price_per_hour = qs[count - 1].avg_price_per_hour
        if not avg_price_per_hour:
            return self.none()

        ids = qs.filter(avg_price_per_hour__lte=avg_price_per_hour).values_list('id', flat=True)
        rand_ids = get_rand_ids(ids)
        return qs.annotate_article_related_fields().filter(id__in=rand_ids)

    def get_new_review_hospital_queryset(self, showing_number=3):
        return self.annotate_article_related_fields().order_by('article_count')[:showing_number]
