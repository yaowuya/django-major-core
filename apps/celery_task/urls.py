from rest_framework.routers import DefaultRouter

from apps.celery_task.views.clocked_task_view import ClockedTaskViewSet
from apps.celery_task.views.periodic_task_view import PeriodicTaskViewSet

routers = DefaultRouter(trailing_slash=True)
# 主机文件版本
routers.register(r"periodic_task", PeriodicTaskViewSet, basename="periodic_task")
routers.register(r"clocked_task", ClockedTaskViewSet, basename="clocked_task")
urlpatterns = []
urlpatterns += routers.urls
