import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestProject.settings')

myapp = Celery('TestProject')

myapp.config_from_object('django.conf:settings', namespace='CELERY')

#
# myapp.conf.beat_schedule = {
#     'my-super-sum-every-5-min' : {
#         'task': 'firstapp.tasks.supper_sum',
#         'schedule': crontab(minute='*/5'),
#         'args': (5, 8),
#     }
# }

myapp.autodiscover_tasks()