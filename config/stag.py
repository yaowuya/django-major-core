# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from config.default import *

# 预发布环境
RUN_MODE = "STAGING"

# 只对预发布环境日志级别进行配置，可以在这里修改
from core.log import set_log_level  # noqa

LOG_LEVEL = "ERROR"
LOGGING = set_log_level(locals())

# 预发布环境数据库可以在这里配置

# 前后端开发模式下支持跨域配置
if FRONTEND_BACKEND_SEPARATION:
    INSTALLED_APPS += ("corsheaders",)  # noqa
    # 该跨域中间件需要放在前面
    MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE  # noqa
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_REPLACE_HTTPS_REFERER = True
    CSRF_TRUSTED_ORIGINS = [
        # may have to include host AND port
        "dev.cwbk.com",
        "dev.cwbk.com:8082",
    ]

DATABASES.update(  # noqa
    {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("BKAPP_DB_NAME", ""),  # 数据库名
            "USER": os.getenv("BKAPP_DB_USERNAME", ""),  # 数据库用户
            "PASSWORD": os.getenv("BKAPP_DB_PASSWORD", ""),  # 数据库密码
            "HOST": os.getenv("BKAPP_DB_HOST", ""),  # 数据库主机
            "PORT": os.getenv("BKAPP_DB_PORT", "3306"),  # 数据库端口
        },
    }
)
