from rest_framework import filters
from dosuri.common import filter_schema as fsc
from django.db.models import Q

# class AddressFilter(fsc.TimeRangeFilter, filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view, now=None):
#         address = view.address
#
#
#         kwargs = self.get_param_kwargs(request, params)
#         now = now or get_current_time_header(request) or None
#         range_from, range_to = get_range_from_request(request, view)
#
#         if not (range_from or range_to):
#             return queryset
#
#         return queryset.filter_by_time_range(range_from, range_to, now=now)


class ForeignUuidFilter(fsc.ForeignUuidFilter, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = view.uuid_filter_params

        kwargs = self.get_param_kwargs(request, params)
        if not kwargs:
            return queryset
        conds = self.get_filter_condition(queryset, kwargs)
        return queryset.filter(**conds).distinct()

    def get_param_kwargs(self, request, params):
        return {param: request.GET.getlist(param)
                for param in params if request.GET.getlist(param)}

    def get_filter_condition(self, queryset, kwargs):
        meta = queryset.model._meta
        conds = {}

        for model_abs_name, uuid_list in kwargs.items():
            chunk = model_abs_name.split('__')
            if len(chunk) > 1:
                conds[f'{model_abs_name}__uuid__in'] = uuid_list
                continue

            model_name = chunk[0]

            field = meta.get_field(model_name)
            obj_ids = self.get_rel_obj_ids(field.related_model, uuid_list)
            conds[f'{model_abs_name}_id__in'] = obj_ids

        return conds

    def get_rel_obj_ids(self, model, uuid_list):
        return list(model.objects.only('id').filter(uuid__in=uuid_list).values_list('id', flat=True))


class ForeignUuidBodyFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = view.uuid_filter_body_params
        kwargs = self.get_param_kwargs(request, params)
        if not kwargs:
            return queryset
        conds = self.get_filter_condition(queryset, kwargs)
        return queryset.filter(**conds).distinct()

    def get_param_kwargs(self, request, params):
        return {param: request.data.get(param)
                for param in params if request.data.get(param)}

    def get_filter_condition(self, queryset, kwargs):
        meta = queryset.model._meta
        conds = {}

        for model_abs_name, uuid_list in kwargs.items():
            chunk = model_abs_name.split('__')
            if len(chunk) > 1:
                conds[f'{model_abs_name}__uuid__in'] = uuid_list
                continue

            model_name = chunk[0]

            field = meta.get_field(model_name)
            obj_ids = self.get_rel_obj_ids(field.related_model, uuid_list)
            conds[f'{model_abs_name}_id__in'] = obj_ids

        return conds

    def get_rel_obj_ids(self, model, uuid_list):
        return list(model.objects.only('id').filter(uuid__in=uuid_list).values_list('id', flat=True))


class UuidSetFilter(fsc.UuidSetFilter, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects
        uuid_list = request.GET.getlist('uuid_set')

        if not uuid_list:
            return queryset

        uuid_list = uuid_list if isinstance(uuid_list, (tuple, list)) else [uuid_list]

        return queryset.filter(uuid__in=uuid_list)


class UuidSetBodyFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects
        uuid_list = request.data.get('uuid')

        if not uuid_list:
            return queryset

        uuid_list = uuid_list if isinstance(uuid_list, (tuple, list)) else [uuid_list]

        return queryset.filter(uuid__in=uuid_list)

class CompleteStatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects

        return queryset.filter(status="Complete")


class InCompleteStatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects

        return queryset.filter(status="InComplete")

class ArticleTypeFilter(fsc.ArticleTypeFilter, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects
        article_type = request.query_params.get('article_type', None)

        if not article_type:
            return queryset

        return queryset.filter(article_type=article_type)

class ArticleSearchFilter(fsc.ArticleSearchFilter, filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Used Django's GET variable to utilize multiple value feature which DRF doesn't provide.
        # note: https://docs.djangoproject.com/en/4.0/ref/request-response/#querydict-objects
        search = request.query_params.get('search', None)

        if not search:
            return queryset
        return queryset.filter(Q(hospital__name__contains=search) | Q(content__contains=search)).order_by('-created_at')