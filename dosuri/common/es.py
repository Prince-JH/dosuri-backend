from elasticsearch import Elasticsearch
from django.conf import settings

cloud_id = 'dosuri:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjQ0MyQ4OWFmZjJhYmVlMTY0YjUxODIxZDQ0N2ExYTdmMGJjNiQzZTFiYzA1YTQxYjM0MWE1YWYyMjhlZTBhMzEzODJiOA=='
user = 'elastic'
pw = 'w6JzEhNIcV6zUySl0pM6M78Y'

client = Elasticsearch(
    cloud_id=settings.cloud_id,
    http_auth=(user, pw)
)
client.search(
    index="test-index"
)
