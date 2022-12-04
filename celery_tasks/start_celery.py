from celery import Celery

celery_task_app = Celery("celery_app", include=["celery_tasks.celery_task"])

celery_task_app.config_from_object("celery_tasks.celery_config")

"""
celery -A celery_tasks.start_celery worker -P eventlet -c 3 -l info
from celery_tasks.celery_task import *
add.delay(5,6);taskA.delay();taskB.delay()
"""
if __name__ == "__main__":
    celery_task_app.start()
