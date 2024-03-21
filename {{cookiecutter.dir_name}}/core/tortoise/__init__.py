# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File： __init__.py
@IDE：PyCharm
@Description：TORTOISE_ORM配置项
"""

from env import setting

TORTOISE_ORM = {
    "connections": {"default": setting.MYSQL_DB_URL},
    "apps": {
        "models": {
            "models": [i for i in setting.MODELS_PATH],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}

