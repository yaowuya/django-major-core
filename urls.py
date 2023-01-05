"""django_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from config import APP_CODE

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^celery_task/", include("apps.celery_task.urls")),
]

if settings.RUN_MODE == "DEVELOP":
    """
    开发时添加SWAGGER API DOC
    访问地址: http://dev.cwbk.com:8000/docs/
    """
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title="%s API" % APP_CODE.upper())
    urlpatterns += [url(r"^docs/$", schema_view)]
