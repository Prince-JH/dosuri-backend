import csv
import requests
from dosuri.hospital import models as hm
from dosuri.community import models as m
from dosuri.user import models as um
from datetime import datetime
from django.core.management.base import BaseCommand
from dosuri.user.utils import get_random_nickname
import multiprocessing
import pandas as pd
from django.db import connection

def add_article(df_list):
    connection.close()
    count=0
    data_len = 5000
    pid=df_list['pid']
    df_list=df_list['df']
    article_list = []
    flag=True
    for idx, row in df_list.iterrows():
        count=count+1
        print(str(pid)+" progress: "+ str((count/data_len)*100) + "%")
        try:
            user=um.User.objects.get(username=row['리뷰어이름'])
            flag=True
        except:
            user=um.User(nickname=get_random_nickname(), is_real=False, username=row['리뷰어이름'])
            user.save()
            flag=False
        if flag:
            continue
        try:
            hospital_id = hm.Hospital.objects.get(code=row['코드']).id
        except:
            hospital_id = None
        org_created_at = row['날짜'][0:-4].replace("\n", "")
        created_at = datetime.strptime(org_created_at, "%Y년 %m월 %d일")
        article_list.append(m.Article(
            user = user,
            status = "complete",
            article_type = "review",
            hospital_id = hospital_id,
            content = row['리뷰내용'],
            created_at = created_at
        ))
    m.Article.objects.bulk_create(article_list, batch_size=1000)

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv('review.csv')
        df_list=[]
        for i in range(0,47):
            df_list.append({
                'pid': i+1,
                'df': df.loc[i*5000:(i+1)*5000, ['리뷰어이름','코드','날짜','리뷰내용']]
            })
            print(str(i*5000)+":"+str((i+1)*5000))
        pool = multiprocessing.Pool(processes=47)
        
        pool.map(add_article, df_list)
        pool.close()
        pool.join()
        print("Successfully Added")
        return
