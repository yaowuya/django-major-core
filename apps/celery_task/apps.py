from django.apps import AppConfig


# 如果你正在使用receiver()装饰器，则可以在应用程序配置类的ready()方法中中导入signals子模块，这将隐式地连接信号处理程序：
class CeleryTaskConfig(AppConfig):
    name = 'apps.celery_task'

    def ready(self):
        from .signals.handlers import (  # noqa
            pre_periodic_task_start_handler,
            periodic_task_start_failed_handler
        )
