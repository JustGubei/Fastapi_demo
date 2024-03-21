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


class User(Items):
    id = fields.IntField(pk=True, description="用户ID")
    user_name = fields.CharField(max_length=50, unique=True, description="账号")
    user_pwd = fields.CharField(max_length=128, description="密码")
    nick_name = fields.CharField(max_length=100, null=True, description="昵称")
    wx_id = fields.CharField(max_length=20, null=True, description="微信号")
    photo = fields.CharField(max_length=255, null=True, description="头像")
    signature = fields.CharField(max_length=255, null=True, description="签名")
    area = fields.CharField(max_length=50, null=True, description="所在区域")
    sex = fields.CharField(max_length=1, null=True, description="性别")
    mobile = fields.CharField(max_length=11, null=True, description="手机号")
    disabled = fields.BooleanField(default=0, null=True, description="是否禁用")
    audit_level = fields.IntField(default=1, null=True, description="审核等级")
    secret = fields.CharField(max_length=64, null=True, description="secret")
    role = fields.OneToOneField('models.Role', related_name='user', null=True)

    class Meta:
        table = "users"
        default_connection = 'default'  # 指定默认连接名称
