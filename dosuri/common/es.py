from django.conf import settings
import time
import json
import datetime
from django.utils.dateparse import parse_datetime
from rest_framework.fields import DateTimeField
from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(settings.ES_ENDPOINT + ':9200', http_auth=(settings.ES_USERNAME, settings.ES_PASSWORD))


# custom middlewawre - factory method pattern

def es_middleware(get_response):
    def middleware(request):
        try:
            start_time = time.time()
            try:
                if request.path == '/swagger' or request.path == '/schema':  ## 스웨거 로깅 X
                    return get_response(request)
                if request.body:
                    request_data = json.loads(request.body.decode())
                else:
                    request_data = {}
            except json.decoder.JSONDecodeError:
                return get_response(request)

            api_failed = False

            if request.GET:
                request_params = dict(request.GET)
            else:
                request_params = {}

            if request.headers:
                request_headers = dict(request.headers)
            else:
                request_headers = {}

            response = get_response(request)
            return response
            
            keys = response.__dict__.keys()
            if request.user.is_authenticated:
                username = request.user.username
            else:
                username = 'anomymous'
            if response.status_code < 200 or response.status_code >= 400:
                api_failed = True

            if "headers" in keys:
                response_headers = dict(response.headers)
            else:
                response_headers = {}

            if "data" in keys:
                try:
                    if 'address' in response.data.keys():
                        if not isinstance(response.data['address'], str):
                            response.data['address'] = response.data['address'].get('large_area', "") + ' ' + \
                                                       response.data['address'].get('small_area', "")
                    response_data = response.data
                except:
                    response_data = {}
            else:
                response_data = {}

            finished_time = time.time()
            execution_time = finished_time - start_time
            data = {
                'HTTP_method': request.method,
                'status_code': response.status_code,
                'is_failed': api_failed,
                'request_body': request_data,
                'request_params': request_params,
                'request_headers': request_headers,
                'username': username,
                'path': request.path,
                'response_headers': response_headers,
                'response_data': response_data,
                "@timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'execution_time': "{:.6f}".format(execution_time),
            }

            try:
                return response
                # es.index(index="api_call_index", body=data)
            except:
                import traceback
                traceback.print_exc()

            return response
        except:
            return get_response(request)

    return middleware
