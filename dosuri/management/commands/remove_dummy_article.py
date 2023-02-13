import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        article_list=m.Article.objects.filter(user_id__in=[1,3,6,10,105941,105945,105958,105962,105964])
        article_list.delete()
        print(article_list)
        print(len(article_list))
        print("Suceessfully Deleted")
        return