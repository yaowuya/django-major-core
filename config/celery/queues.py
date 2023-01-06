from typing import Any, List

from kombu import Exchange, Queue


class ScalableQueues(object):
    _queues = {}

    @classmethod
    def queues(cls):
        return cls._queues

    @classmethod
    def add(cls, name, routing_key="", queue_arguments=None):
        queue_arguments = queue_arguments or {}
        cls._queues[name] = {"name": name, "routing_key": routing_key or name, "queue_arguments": queue_arguments}

    @classmethod
    def has_queue(cls, queue):
        return queue in cls._queues

    @classmethod
    def routing_key_for(cls, queue):
        return cls._queues[queue]["routing_key"]


class QueueResolver:
    def __init__(self, queue: str):
        self.queue = queue

    def resolve_task_queue_and_routing_key(self, task: Any) -> (str, str):
        task_name = task
        if not isinstance(task_name, str):
            task_name = task.name

        queue_config = self.routes_config()
        return queue_config[task_name]["queue"], queue_config[task_name]["routing_key"]

    def routes_config(self) -> dict:
        suffix = "_%s" % self.queue if self.queue else ""
        return {
            "pipeline.eri.celery.tasks.execute": {
                "queue": "er_execute%s" % suffix,
                "routing_key": "er_execute%s" % suffix,
            },
            "pipeline.eri.celery.tasks.schedule": {
                "queue": "er_schedule%s" % suffix,
                "routing_key": "er_schedule%s" % suffix,
            },
        }

    def queues(self) -> List[Queue]:
        exchange = Exchange("default", type="direct")
        return [
            Queue(queue_config["queue"], exchange, routing_key=queue_config["routing_key"], max_priority=255)
            for queue_config in self.routes_config().values()
        ]


CELERY_QUEUES = QueueResolver("").queues()
