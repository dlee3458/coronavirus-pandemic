from __future__ import absolute_import, unicode_literals

import os 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid19.settings')
app = Celery('covid19')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'get-stats': {
        'task': 'stats',
        'schedule': crontab(minute=10, hour=4),
    },
    'get-countries': {
        'task': 'countries',
        'schedule': crontab(minute=10, hour=4),
    },
    'get-trending': {
        'task': 'trending',
        'schedule': crontab(minute=10, hour=4),
    },
    'get-new': {
        'task': 'new',
        'schedule': crontab(minute=10, hour=4),
    },
    'get-rate': {
        'task': 'rate',
        'schedule': crontab(minute=10, hour=4)
    },
    'state-stats': {
        'task': 'states',
        'schedule': crontab(minute=6, hour=4)
    }
}