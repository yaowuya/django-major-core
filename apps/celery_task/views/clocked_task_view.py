from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.celery_task.models.clocked_task import ClockedTask
from apps.celery_task.serializers.cloced_task_serializer import ClockedTaskSerializer
from packages.drf.pagination import CustomPageNumberPagination
from packages.drf.renderers import CustomRenderer
from packages.drf.viewsets import ModelViewSet


class ClockedTaskViewSet(ModelViewSet):
    queryset = ClockedTask.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ClockedTaskSerializer
    pagination_class = CustomPageNumberPagination
    renderer_classes = (CustomRenderer,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "creator": ["exact"],
        "plan_start_time": ["gte", "lte"],
        "task_name": ["exact", "icontains", "contains"]
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["creator"] = request.user.username or "system"
        task = ClockedTask.objects.create_task(**validated_data)
        response_serializer = self.serializer_class(instance=task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
