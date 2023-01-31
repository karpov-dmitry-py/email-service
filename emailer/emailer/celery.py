from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailer.settings')

from django.conf import settings

app = Celery('emailer', include=['app.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def add(x, y):
    return x / y
