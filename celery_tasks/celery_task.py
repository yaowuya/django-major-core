import socket
import time

from celery_tasks.start_celery import celery_task_app


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


@celery_task_app.task
def add(x, y):
    time.sleep(3)  # 模拟耗时操作
    s = x + y
    print("主机IP {}: x + y = {}".format(get_host_ip(), s))
    return s


@celery_task_app.task
def taskA():
    print("taskA")
    time.sleep(3)


@celery_task_app.task
def taskB():
    print("taskB")
    time.sleep(3)
