from __future__ import absolute_import, unicode_literals
import os
from .celery_app import app as celery_app

# Set default settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DAP_DJANGO_APP.settings')

app = celery_app('DAP_DJANGO_APP')

# Using a string means the worker doesn't need to serialize the object
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()

# Add the Celery Beat scheduler
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'