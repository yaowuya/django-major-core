from django.dispatch import Signal

pre_periodic_task_start = Signal(providing_args=["periodic_task", "pipeline_instance"])
periodic_task_start_failed = Signal(providing_args=["periodic_task", "history"])