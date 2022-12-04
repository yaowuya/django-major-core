## 启动

在`django_core`目录下启动项目

### 启动命令

```python
celery -A myCeleryProj.app worker -c 3 -l info
```

`-c 3`表示启用三个子进程执行该队列中的任务。运行结果如下：

```python
(venv) PS D:\01-code\django_core> celery -A celery_app.start_celery worker -c 3 -l info
 
 -------------- celery@zhongrf v4.4.0 (cliffs)
--- ***** -----
-- ******* ---- Windows-10-10.0.22000-SP0 2022-12-04 15:28:52
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         celery_app:0x1fbf249e048
- ** ---------- .> transport:   redis://127.0.0.1:6379/0
- ** ---------- .> results:     redis://127.0.0.1:6379/0
- *** --- * --- .> concurrency: 3 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . celery_app.tasks.task1.add

[2022-12-04 15:28:52,189: INFO/MainProcess] Connected to redis://127.0.0.1:6379/0
[2022-12-04 15:28:52,189: INFO/MainProcess] mingle: searching for neighbors
[2022-12-04 15:28:52,424: INFO/SpawnPoolWorker-1] child process 63380 calling self.run()
[2022-12-04 15:28:52,439: INFO/SpawnPoolWorker-2] child process 61552 calling self.run()
[2022-12-04 15:28:52,439: INFO/SpawnPoolWorker-3] child process 60512 calling self.run()
[2022-12-04 15:28:53,206: INFO/MainProcess] mingle: all alone
[2022-12-04 15:28:53,206: INFO/MainProcess] celery@zhongrf ready.

```

更多启动Celery worker的方法如下:

```python
# 设置处理任务队列的子进程个数为10。
celery -A myCeleryProj.app worker -c10 -l info 
# 设置处理任务队列为web_task。
celery -A myCeleryProj.app worker -Q web_task -l info 
# 设置后台运行并指定日志文件位置。
celery -A myCeleryProj.app worker –logfile /tmp/celery.log -l info -D
```

在window环境，`celery4`不支持多启动多个worker，需要加上`eventlet`

```python
celery -A myCeleryProj.app worker -P eventlet -c10 -l info 
```

### 调用task的方法有以下三种

#### 1.使用`apply_async(args[, kwargs[, …]])`发送一个task到任务队列

支持更多的控制，如`add.apply_async(countdown=10)`表示执行add函数的时间限制最多为10秒；

`add.apply_async(countdown=10, expires=120)`表示执行add函数的时间限制最多为10秒，add函数的有效期为120秒；

`add.apply_async(expires=now + timedelta(days=2))`表示执行add函数的有效期为两天。使用`apply_async`还支持回调，假如任务函数如下：

```python
@app.task
def add(x, y):
return x + y
```

那么

```python
add.apply_async((2, 2), link=add.s(16))  # 就相当于(2 + 2) + 16 = 20。
```

#### 2.使用`delay(*args, **kwargs)`

该方法是`apply_async`的快捷方式，提供便捷的异步调度，但是如果想要更多的控制，就必须使用方法1。使用delay就像调用普通函数那样，非常简便，如下所示。

```python
task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
```

#### 3.直接调用，相当于普通的函数调用，不在worker上执行。

