
from django.core.management.base import BaseCommand
import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
import numpy as np
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        seed = 0
        nickname_list = []
        tmp_user_list = []
        while len(nickname_list) < 106000:
            seed = seed + 1
            print(len(nickname_list))
            nickname_list = list(set(nickname_list + self.get_nickname_list(seed))) ## 중복 제거
        print(len(nickname_list))
        count = 0
        with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
            user_list = []
            data_len = 177402
            for row in spamreader:
                count = count+1
                print("progress:"+str(int((count/data_len) * 100)) + "%")
                if len(nickname_list) == 0:
                    seed = seed
                    nickname_list = self.get_nickname_list(nickname_len, seed)
                
                if row[2] not in tmp_user_list:
                    user_list.append(um.User(nickname=nickname_list.pop(), tmp_review_username=row[2], is_real=False, username="crowl_review_user_"+str(count)))
                    tmp_user_list.append(row[2])
        print(len(user_list))
        um.User.objects.bulk_create(user_list, batch_size=1000)
        print("Successfully Added")
        return
    def get_nickname_list(self, seed):
        return requests.get('https://nickname.hwanmoo.kr/?format=json&count=3000&max_length=12&seed='+str(seed)).json()['words']