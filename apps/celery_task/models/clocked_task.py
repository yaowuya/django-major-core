import json

from django.db import models, transaction
from django_celery_beat.models import (
    PeriodicTask as DjangoCeleryBeatPeriodicTask,
    ClockedSchedule as DjangoCeleryBeatClockedSchedule,
)

from commons.common_model import MaintainerInfo
from commons.utils.uniqid import uniqid


class ClockedTaskManager(models.Manager):
    def create_task(self, **kwargs):
        task_name = kwargs["task_name"]
        plan_start_time = kwargs["plan_start_time"]
        creator = kwargs["creator"]
        task_params = kwargs["task_params"]
        with transaction.atomic():
            clocked, _ = DjangoCeleryBeatClockedSchedule.objects.get_or_create(clocked_time=plan_start_time)
            task = ClockedTask.objects.create(
                task_name=task_name,
                creator=creator,
                plan_start_time=plan_start_time,
                task_params=task_params
            )
            clocked_task_kwargs = {"clocked_task_id": task.id}
            clocked_task = DjangoCeleryBeatPeriodicTask.objects.create(
                clocked=clocked,
                name=task_name + uniqid(),
                task="gcloud.clocked_task.tasks.clocked_task_start",
                one_off=True,
                kwargs=json.dumps(clocked_task_kwargs),
            )
            task.clocked_task_id = clocked_task.id
            task.save()
        return task


class ClockedTask(MaintainerInfo):
    task_name = models.CharField(help_text="任务名称", max_length=128)
    clocked_task_id = models.IntegerField(help_text="计划任务 Celery任务 ID", null=True)
    creator = models.CharField(help_text="计划任务创建人", max_length=32)
    plan_start_time = models.DateTimeField(help_text="计划任务启动时间", db_index=True)
    task_params = models.TextField(help_text="任务创建相关数据", null=True)
    objects = ClockedTaskManager()

    class Meta:
        verbose_name = verbose_name_plural = "计划任务"
        ordering = ["-id"]
