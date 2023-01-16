import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
from datetime import datetime
from django.core.management.base import BaseCommand
from pytz import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        data_len = 177402
        count = 0
        failed_article=[]
        with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
            for row in spamreader:
                count=count+1
                print("progress:"+str(int((count/data_len) * 100)) + "%")
                org_created_at = row[4][0:-4].replace("\n", "")
                created_at = datetime.strptime(org_created_at, "%Y년 %m월 %d일")
                print(row[3])
                try:
                    article=m.Article.objects.get(content=row[3])
                    article.created_at=created_at
                    article.save()
                except:
                    print(failed_article)
                    failed_article.append(row)
        print("Successfully Updated")
        
        with open("failed.txt", "w") as txt_file:
            for line in failed_article:
                for i in line:
                    txt_file.write(" ".join(i) + "\n") # works with any number of elements in a line
        return
