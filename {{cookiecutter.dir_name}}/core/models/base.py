# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：base.py
@IDE：PyCharm
@Description：基类
"""

import datetime

from tortoise import fields, models


class Items(models.Model):
    """
    @summary: Orm抽象基类
    """
    id = fields.IntField(pk=True, index=True)
    is_delete = fields.IntField(description="0=未删, 1=已删", default=0)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True  # 抽象模型，用于继承

    def to_dict(self):
        # 获取对象映射
        data = {field: getattr(self, field) for field in self._meta.fields}
        if type(data.get('created_at')) is datetime.datetime:
            data['created_at'] = data['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            data['updated_at'] = data['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        return data
