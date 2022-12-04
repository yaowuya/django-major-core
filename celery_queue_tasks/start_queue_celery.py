from celery import Celery

queue_task_app = Celery("celery_queue_app", include=["celery_queue_tasks.celery_queue_task"])
# queue_task_app.conf.task_routes = {
#     "myCeleryProj.tasks.add", {"queue": "default"},
#     "myCeleryProj.tasks.taskA", {"queue": "tasks_A"},
#     "myCeleryProj.tasks.taskB", {"queue": "tasks_B"}
# }
queue_task_app.config_from_object("celery_queue_tasks.celery_queue_config")
"""
celery -A celery_queue_tasks.start_queue_celery worker -Q tasks_A,tasks_B -P eventlet -c 3 -l info
from celery_tasks.celery_task import *
add.delay(5,6);taskA.delay();taskB.delay()
"""
if __name__ == "__main__":
    queue_task_app.start()
