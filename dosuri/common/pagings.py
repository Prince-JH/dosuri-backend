from rest_framework.pagination import PageNumberPagination


class PageSizeResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'