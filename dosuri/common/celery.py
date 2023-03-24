from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab 
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
app = Celery('dosuri')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    BROKER_URL='django://',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
    'article_relocation_every_day': {  
        'task': 'dosuri.tasks.article_relocation_every_day',   
        'schedule': crontab(hour=23, minute=59),      
        'args': () 
    },
    'test_batch_every_min': {  
        'task': 'dosuri.tasks.test_batch_every_min',   
        'schedule': crontab(), 
        'args': ()       
    },
    }
)
app.autodiscover_tasks()