import os

from celery import Celery
from celery.app.log import TaskFormatter
from celery.signals import after_setup_logger
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basedjango.settings')
app = Celery('basedjango')
CELERY_TIMEZONE = settings.TIME_ZONE
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([
    'apps.celery_tasks.background_tasks',
    'apps.celery_tasks.scheduled_tasks',
])


@after_setup_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(
            TaskFormatter(
                '{"time": "%(asctime)s", "task_id": "%(task_id)s", "task_name": "%(task_name)s", "name": "%(name)s", '
                '"levelname": "%(levelname)s", "msg": "%(message)s"}', use_color=False))
