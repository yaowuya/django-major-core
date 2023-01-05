from rest_framework import serializers

from apps.celery_task.models import PeriodicTask


class PeriodicTaskSerializer(serializers.ModelSerializer):
    last_run_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S %z", read_only=True)

    class Meta:
        model = PeriodicTask
        fields = "__all__"


class CreatePeriodicTaskSerializer(serializers.ModelSerializer):
    cron = serializers.DictField(write_only=True)
    name = serializers.CharField()

    class Meta:
        model = PeriodicTask
        fields = ["name", "cron"]
