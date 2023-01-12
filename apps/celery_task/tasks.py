import datetime
import json
import traceback

import pytz
from celery.task import task
from django.utils import timezone

from apps.celery_task import signals
from apps.celery_task.models import PeriodicTask, PeriodicTaskHistory
from apps.celery_task.models.clocked_task import ClockedTask
from commons.log import celery_logger


@task(ignore_result=True)
def periodic_task_start(*args, **kwargs):
    celery_logger.info("periodic_task_start 执行")
    celery_logger.info(f"params:{kwargs}")
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
        celery_logger.error(et)
        PeriodicTaskHistory.objects.record_schedule(
            periodic_task=periodic_task, pipeline_instance=None, ex_data=et, start_success=False,
        )
        return
    periodic_task.total_run_count += 1
    periodic_task.last_run_at = timezone.now()
    periodic_task.save()
    PeriodicTaskHistory.objects.record_schedule(periodic_task=periodic_task, ex_data="")


@task(gnore_result=True)
def clocked_task_start(clocked_task_id, *args, **kwargs):
    try:
        celery_logger.info("clocked_task_start 运行")
        clocked_task = ClockedTask.objects.get(id=clocked_task_id)
    except ClockedTask.DoesNotExist:
        # task has been deleted
        celery_logger.warning(f"[clocked_task_start] clocked task {clocked_task_id} not found, may be deleted.")
        return
    task_params = json.loads(clocked_task.task_params)
    celery_logger.info(f"clocked_task_start 参数 {task_params}")


@task(ignore_result=True)
def create_job_task(x, y):
    """创建作业任务"""
    celery_logger.info(f"{x},{y},create_job_task")


@task(ignore_result=True)
def parse_job_task(*args, **kwargs):
    celery_logger.info("parse_job_task")
