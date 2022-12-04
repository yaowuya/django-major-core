from celery import Celery

celery_beat_app = Celery("celery_beat", include=["celery_beat_tasks.celery_beat_task"])

celery_beat_app.config_from_object("celery_beat_tasks.celery_beat_config")

"""
 celery -A celery_beat_tasks.start_celery_beat beat -l info
"""
if __name__ == "__main__":
    celery_beat_app.start()
