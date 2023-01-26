import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        failed_user = []
        data_len = 177402
        count = 0
        with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
            article_list = []
            default_hospital = hm.Hospital.objects.get(id=7379)
            for row in spamreader:
                count=count+1
                print("progress:"+str(int((count/data_len) * 100)) + "%")
                try:
                    hospital = hm.Hospital.objects.get(code=row[0])
                except:
                    hospital = default_hospital
                org_created_at = row[4][0:-4].replace("\n", "")
                print(row[2])
                created_at = datetime.strptime(org_created_at, "%Y년 %m월 %d일")
                try:
                    user = um.User.objects.get(tmp_review_username=row[2])
                    article_list.append(m.Article(
                        user = um.User.objects.get(tmp_review_username=row[2]),
                        status = "complete",
                        article_type = "review",
                        hospital = hospital,
                        content = row[3],
                        created_at = created_at
                    ))
                except:
                    failed_user.append(row[2])
        
        m.Article.objects.bulk_create(article_list, batch_size=1000)
        print(failed_user)
        print("Successfully Added")
        with open("output.txt", "w") as txt_file:
            for line in failed_user:
                txt_file.write(" ".join(line) + "\n") # works with any number of elements in a line
        return

    def add_article(self, index):
        data_len = 10000
        count = 0
        if index==17:
            end=177402
        else:
            end=(index+1)*10000
        with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
            article_list = []
            default_hospital = hm.Hospital.objects.get(id=7379)
            for row in islice(spamreader,index*10000,end):
                count=count+1
                print("index:"+str(index))
                print("progress:"+str(int((count/data_len) * 100)) + "%")
                try:
                    hospital = hm.Hospital.objects.get(code=row[0])
                except:
                    hospital = default_hospital
                org_created_at = row[4][0:-4].replace("\n", "")
                created_at = datetime.strptime(org_created_at, "%Y년 %m월 %d일")
                article_list.append(m.Article(
                    user = um.User.objects.get(tmp_review_username=row[2]),
                    status = "complete",
                    article_type = "review",
                    hospital = hospital,
                    content = row[3],
                    created_at = created_at
                ))
        
        m.Article.objects.bulk_create(article_list, batch_size=1000)
        print("Successfully Added")
        return
