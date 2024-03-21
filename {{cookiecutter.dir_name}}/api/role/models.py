# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：models.py
@IDE：PyCharm
@Description：
"""

from tortoise import fields, models

from core.models.base import Items


class Role(Items):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    permissions = fields.ReverseRelation["Permission"]  # 注意这里是小写，反向关系使用 ReverseRelation


class Permission(Items):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    role = fields.ForeignKeyField("models.Role", related_name="permissions")  # 使用 ForeignKeyField 来表示外键关系
