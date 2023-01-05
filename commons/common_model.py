# -*- coding: utf-8 -*-
from django.db import models


class TimeInfo(models.Model):
    """
    Add time fields to another models.
    """

    class Meta:
        verbose_name = "时间相关字段"
        abstract = True

    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("修改时间", auto_now=True)


class MaintainerInfo(models.Model):
    """
    Add maintainer fields to another models.
    """

    class Meta:
        verbose_name = "维护者相关字段"
        abstract = True

    created_by = models.CharField("创建者", max_length=32, default="")
    updated_by = models.CharField("更新者", max_length=32, default="")
