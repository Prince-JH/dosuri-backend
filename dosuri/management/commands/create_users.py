
from django.core.management.base import BaseCommand
import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
from dosuri.user.utils import get_random_nickname
import random
import multiprocessing
import pandas as pd
from django.db import connection


def add_user(df_list):
    connection.close()
    count=0
    data_len = 10000
    pid=df_list['pid']
    df_list=df_list['df']
    for idx, row in df_list.iterrows():
        count=count+1
        print(str(pid)+" progress: "+ str((count/data_len)*100) + "%")
        if not um.User.objects.filter(username=row['리뷰어이름']).exists():
            user=um.User(nickname=get_random_nickname(), is_real=False, username=row['리뷰어이름'])
            user.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        um.User.objects.filter(is_real=False).delete()
        df = pd.read_csv('review.csv')
        df_list=[]
        for i in range(0,24):
            df_list.append({
                'pid': i+1,
                'df': df.loc[i*10000:(i+1)*10000, ['리뷰어이름']]
            })
        pool = multiprocessing.Pool(processes=25)
        
        pool.map(add_user, df_list)
        pool.close()
        pool.join()
        print("Successfully Added")
        return