
from django.core.management.base import BaseCommand
import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
import numpy as np

class Command(BaseCommand):
    def handle(self, *args, **options):
        seed = 0
        nickname_list = self.get_nickname_list(seed)
        tmp_user_list = []
        count = 0
        with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
            user_list = []
            data_len = 177402
            for row in spamreader:
                count = count+1
                print("progress:"+str((count/data_len) * 100))
                username = row[2]
                if len(nickname_list) == 0:
                    nickname_list = self.get_nickname_list(seed)
                
                if row[3] not in tmp_user_list:
                    user_list.append(um.User(nickname=nickname_list.pop(), tmp_review_username=row[3], is_real=False))
                    tmp_user_list.append(row[3])
        um.User.objects.bulk_create(user_list, batch_size=1000)
        print(user_list)
        print("Successfully Added")
        return
    def get_nickname_list(self, seed):
        return requests.get('https://nickname.hwanmoo.kr/?format=json&count=100&max_length=6&seed='+str(seed)).json()['words']