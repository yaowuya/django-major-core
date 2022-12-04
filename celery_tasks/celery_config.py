BROKER_URL = 'redis://127.0.0.1:6379/0'  # 使用redis 作为消息代理

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 任务结果存在Redis

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
