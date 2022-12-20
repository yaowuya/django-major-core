# Celery Beat任务调度

**Celery Beat是Celery的调度器，其定期启动任务，然后由集群中的可用工作节点worker执行这些任务。**

默认情况下，Beat进程读取配置文件中`CELERYBEAT_SCHEDULE`的设置，也可以使用自定义存储，比如将启动任务的规则存储在`SQL`数据库中。请确保每次只为调度任务运行一个调度程序，否则任务将被重复执行。使用集群的方式意味着调度不需要同步，服务可以在不使用锁的情况下运行。

先明确一个概念——时区。间隔性任务调度默认使用`UTC`时区，也可以通过时区设置来改变时区。例如：

```python
CELERY_TIMEZONE = 'Asia/Shanghai'  # 通过配置文件设置
app.conf.timezone = 'Asia/Shanghai' #直接在Celery app的源代码中设置
```

时区的设置必须加入`Celery`的`App`中，默认的调度器（将调度计划存储在`celerybeat-schedule`文件中）将自动检测时区是否改变，如果时区改变，则自动重置调度计划。其他调度器可能不会自动重置，比如`Django`数据库调度器就需要手动重置调度计划。

### 配置

```python
from datetime import timedelta

from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379/0'  # 使用redis 作为消息代理

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 任务结果存在Redis

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    "add": {
        "task": "celery_beat_tasks.celery_beat_task.add",
        "schedule": timedelta(seconds=10),  # 定义间隔为10s的任务
        "args": (10, 16),
    },
    "taskA": {
        "task": "celery_beat_tasks.celery_beat_task.taskA",
        "schedule": crontab(hour=19, minute=50),  # 定义间隔为对应时区下21：11分执行的任务
    },
    "taskB": {
        "task": "celery_beat_tasks.celery_beat_task.taskB",
        "schedule": crontab(hour=21, minute=8),  # 定义间隔为对应时区下21：8分执行的任务
    },
}

```

### 启用

启用Celery Beat进程处理调度任务

```python
celery -A celery_beat_tasks.start_celery_beat beat -l info
```

最后可以在worker界面看到定时或间隔任务的处理情况

```python
celery -A celery_beat_tasks.start_celery_beat worker -P eventlet -c 3 -l info 
```
