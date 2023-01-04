import json

from django.db import models
from django_celery_beat.models import (
    PeriodicTask as DjangoCeleryBeatPeriodicTask,
    CrontabSchedule as DjangoCeleryBeatCrontabSchedule,
)

# Create your models here.
from apps.celery_task.constants import CELERY_DEFAULT_PRIORITY
from apps.celery_task.signals import periodic_task_start_failed
from commons.utils.uniqid import uniqid


class PeriodicTaskManager(models.Manager):
    def create_task(
            self,
            name,
            cron,
            creator,
            timezone=None,
            spread=False,
            priority=CELERY_DEFAULT_PRIORITY,
            queue="",
            trigger_task="",
    ):
        schedule, _ = DjangoCeleryBeatCrontabSchedule.objects.get_or_create(
            minute=cron.get("minute", "*"),
            hour=cron.get("hour", "*"),
            day_of_week=cron.get("day_of_week", "*"),
            day_of_month=cron.get("day_of_month", "*"),
            month_of_year=cron.get("month_of_year", "*"),
            timezone=timezone or "UTC",
        )
        _ = schedule.schedule  # noqa

        task = self.create(
            name=name,
            cron=schedule.__str__(),
            creator=creator,
            priority=priority,
            queue=queue,
        )

        kwargs = {"period_task_id": task.id, "spread": spread}
        celery_task = DjangoCeleryBeatPeriodicTask.objects.create(
            crontab=schedule,
            name=uniqid(),
            task=trigger_task or "pipeline.contrib.periodic_task.tasks.periodic_task_start",
            enabled=False,
            kwargs=json.dumps(kwargs),
        )
        task.celery_task = celery_task
        task.save()
        return task


class PeriodicTask(models.Model):
    name = models.CharField(verbose_name="周期任务名称", max_length=64)
    cron = models.CharField(verbose_name="调度策略", max_length=128)
    celery_task = models.ForeignKey(DjangoCeleryBeatPeriodicTask, verbose_name="celery 周期任务实例", null=True,
                                    on_delete=models.SET_NULL)
    total_run_count = models.PositiveIntegerField(verbose_name="执行次数", default=0)
    last_run_at = models.DateTimeField(verbose_name="上次运行时间", null=True)
    creator = models.CharField(verbose_name="创建者", max_length=32, default="")
    priority = models.IntegerField(verbose_name="流程优先级", default=CELERY_DEFAULT_PRIORITY)
    queue = models.CharField(verbose_name="流程使用的队列名", max_length=512, default="")

    objects = PeriodicTaskManager()


class PeriodicTaskHistoryManager(models.Manager):
    def record_schedule(self, periodic_task, ex_data, start_success=True):
        history = self.create(
            periodic_task=periodic_task,
            ex_data=ex_data,
            start_success=start_success,
            priority=periodic_task.priority,
            queue=periodic_task.queue,
        )

        if not start_success:
            periodic_task_start_failed.send(sender=PeriodicTask, periodic_task=periodic_task, history=history)

        return history


class PeriodicTaskHistory(models.Model):
    periodic_task = models.ForeignKey(
        PeriodicTask, related_name="instance_rel", verbose_name="周期任务", null=True, on_delete=models.DO_NOTHING,
    )
    ex_data = models.TextField("异常信息")
    start_at = models.DateTimeField("开始时间", auto_now_add=True)
    start_success = models.BooleanField("是否启动成功", default=True)
    priority = models.IntegerField("流程优先级", default=CELERY_DEFAULT_PRIORITY)
    queue = models.CharField("流程使用的队列名", max_length=512, default="")

    objects = PeriodicTaskHistoryManager()
