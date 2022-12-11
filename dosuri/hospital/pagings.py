from rest_framework.utils.urls import replace_query_param, remove_query_param

def make_response_with_paging(view, data):
    res = {}
    res['count'] = len(data)
    page = int(view.request.GET.get('page', 1))
    res['next'] = get_next_link(view, page)
    res['prev'] = get_previous_link(view, page)
    res['result'] = data
    return res


def get_next_link(view, page):
    url = view.request.build_absolute_uri()
    page_number = page + 1
    return replace_query_param(url, view.page_query_param, page_number)


def get_previous_link(view, page):
    url = view.request.build_absolute_uri()
    page_number = page - 1
    if page_number == 0:
        return remove_query_param(url, view.page_query_param)
    return replace_query_param(url, view.page_query_param, page_number)
