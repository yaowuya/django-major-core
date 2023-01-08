from datetime import timedelta

from celery.schedules import crontab
from kombu import Exchange, Queue

default_exchange = Exchange("default", type="direct")

# 设置时区
CELERY_TIMEZONE = "Asia/Shanghai"
# 启动时区设置
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False

CELERY_DEFAULT_PRIORITY = 100
CELERY_MIN_PRIORITY = 0
CELERY_MAX_PRIORITY = 255

# 创建作业
CREATE_JOB_QUEUE_NAME = "create_job_queue"
CREATE_JOB_ROUTING_KEY = "create_job_key"
# 解析作业
PARSE_JOB_QUEUE_NAME = "parse_job_queue"
PARSE_JOB_ROUTING_KEY = "parse_job_key"

CREATE_JOB_ROUTING = {
    "queue": CREATE_JOB_QUEUE_NAME,
    "routing_key": CREATE_JOB_ROUTING_KEY
}
PARSE_JOB_ROUTING = {
    "queue": PARSE_JOB_QUEUE_NAME,
    "routing_key": PARSE_JOB_ROUTING_KEY
}

# 路由
CELERY_ROUTES = {
    # 创建作业
    "apps.celery_task.tasks.create_job_task": CREATE_JOB_ROUTING,
    # 解析作业
    "apps.celery_task.tasks.parse_job_task": PARSE_JOB_ROUTING,
}
# 队列
CELERY_QUEUES = [
    # keep old queue to process message left in broker, remove on next version
    Queue("default", default_exchange, routing_key="default"),
    Queue(
        CREATE_JOB_QUEUE_NAME,
        default_exchange,
        routing_key=CREATE_JOB_ROUTING_KEY,
        queue_arguments={"x-max-priority": CELERY_MAX_PRIORITY},
    ),
    Queue(
        PARSE_JOB_QUEUE_NAME,
        default_exchange,
        routing_key=PARSE_JOB_ROUTING_KEY,
        queue_arguments={"x-max-priority": CELERY_MAX_PRIORITY},
    ),
]

CELERY_DEFAULT_QUEUE = "default"  # 默认队列
CELERY_DEFAULT_EXCHANGE = "default"  # 默认 exchange
CELERY_DEFAULT_ROUTING_KEY = "default"  # 默认routing key

# 定时任务测试
CELERYBEAT_SCHEDULE = {
    'create_job_task': {
        'task': 'apps.celery_task.tasks.create_job_task',
        'schedule': timedelta(seconds=20),
        'args': (1, 10)
    },
    'parse_job_task': {
        'task': 'apps.celery_task.tasks.parse_job_task',
        'schedule': crontab(minute='*/2'),
        'args': ()
    }
}