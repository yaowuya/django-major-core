from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, platforms
from django.conf import settings

# First steps with Django
# Using Celery with Django https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

# http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#running-the-worker-with-superuser-privileges-root
# for root start celery

platforms.C_FORCE_ROOT = True

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("project_celery")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {!r}".format(self.request))
