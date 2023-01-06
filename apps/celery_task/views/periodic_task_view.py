from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.celery_task.models import PeriodicTask
from apps.celery_task.serializers.periodic_task_serializer import PeriodicTaskSerializer, CreatePeriodicTaskSerializer
from packages.drf.pagination import CustomPageNumberPagination
from packages.drf.renderers import CustomRenderer
from packages.drf.viewsets import ModelViewSet
from django_filters import FilterSet


class PeriodicTaskFilter(FilterSet):
    class Meta:
        model = PeriodicTask
        fields = {"name": ["exact"], "creator": ["contains"]}


class PeriodicTaskViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    pagination_class = CustomPageNumberPagination
    renderer_classes = (CustomRenderer,)
    filter_class = PeriodicTaskFilter
    ordering_fields = ["id"]
    ordering = ["-id"]

    def create(self, request, *args, **kwargs):
        serializer = CreatePeriodicTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        creator = "test"
        serializer.validated_data["name"] = name
        serializer.validated_data["creator"] = creator
        instance = serializer.save()
        instance.set_enabled(True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def create_task(self, request, *args, **kwargs):
        """创建任务
        {
          "name": "test",
          "cron": {"minute":"*/5","hour":"*","day_of_week":"*","day_of_month":"*","month_of_year":"*"},
        }
        """
        params = request.data
        cron_data = params.get("cron")
        name = params.get("name")
        creator = params.get("creator", "test")
        periodic_task = PeriodicTask.objects.create_task(name, cron_data, creator)
        periodic_task.set_enabled(True)
        return Response({"result": "创建成功"})
