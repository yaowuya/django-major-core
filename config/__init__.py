import os
from core.celery import celery_app

__all__ = ["celery_app", "BASE_DIR", "APP_CODE"]

# 项目的唯一code
APP_CODE = "django_core"


# app 基本信息
def get_env_or_raise(key):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(
            ('Environment variable "{}" not found, you must set this variable to run this application.').format(key)
        )
    return value


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
