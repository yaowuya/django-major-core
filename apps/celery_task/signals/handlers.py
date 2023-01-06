import traceback

from django.dispatch import receiver

from commons.log import logger, celery_logger
from apps.celery_task.models import PeriodicTask
from apps.celery_task.signals import periodic_task_start_failed, pre_periodic_task_start


@receiver(pre_periodic_task_start, sender=PeriodicTask)
def pre_periodic_task_start_handler(sender, periodic_task, pipeline_instance, **kwargs):
    """任务开启之前做点什么"""
    celery_logger.info("任务开启之前做点什么")


@receiver(periodic_task_start_failed, sender=PeriodicTask)
def periodic_task_start_failed_handler(sender, periodic_task, history, **kwargs):
    try:
        # send_periodic_task_message(periodic_task, history)
        celery_logger.info("send_periodic_task_message")
    except Exception:
        logger.error(
            "periodic_task_start_failed_handler send message error: %s" % (traceback.format_exc())
        )
