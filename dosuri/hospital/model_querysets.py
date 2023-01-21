from datetime import date

from django.db.models import QuerySet, Count, Subquery, OuterRef
from django.db.models.functions import Coalesce

from dosuri.common import models as cm
from dosuri.community import constants as cmc
from django.apps import apps


class HospitalQuerySet(QuerySet):
    def annotate_extra_fields(self):
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
