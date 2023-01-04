import datetime
import traceback

import pytz
from celery.task import task
from django.utils import timezone

from apps import logger
from apps.celery_task import signals
from apps.celery_task.models import PeriodicTask, PeriodicTaskHistory


@task(ignore_result=True)
def periodic_task_start(*args, **kwargs):
    try:
        periodic_task = PeriodicTask.objects.get(id=kwargs["period_task_id"])
    except PeriodicTask.DoesNotExist:
        # task has been deleted
        return
    try:
        tz = periodic_task.celery_task.crontab.timezone
        now = datetime.datetime.now(tz=pytz.utc).astimezone(tz)
        signals.pre_periodic_task_start.send(
            sender=PeriodicTask, periodic_task=periodic_task, pipeline_instance=None
        )
    except Exception:
        et = traceback.format_exc()
        logger.error(et)
        PeriodicTaskHistory.objects.record_schedule(
            periodic_task=periodic_task, pipeline_instance=None, ex_data=et, start_success=False,
        )
        return
    periodic_task.total_run_count += 1
    periodic_task.last_run_at = timezone.now()
    periodic_task.save()
    PeriodicTaskHistory.objects.record_schedule(periodic_task=periodic_task, ex_data="")
