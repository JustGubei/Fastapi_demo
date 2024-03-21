# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：models.py
@IDE：PyCharm
@Description：
"""

from core.models.base import Items
from tortoise import fields

class Logs(Items):
    id = fields.IntField(pk=True)
    user = fields.CharField(max_length=255, null=True)
    api = fields.CharField(max_length=255, null=True)
    method = fields.CharField(max_length=10, null=True)
    params = fields.JSONField(null=True)
    status_code = fields.CharField(max_length=255, null=True)
    action = fields.CharField(max_length=255, null=True)
    ip = fields.CharField(max_length=32, null=True)
    response_time = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "logs"


