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
