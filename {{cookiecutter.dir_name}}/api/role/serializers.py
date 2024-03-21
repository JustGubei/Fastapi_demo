# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：serializers.py
@IDE：PyCharm
@Description：
"""

from pydantic import BaseModel


class RoleCreateSchema(BaseModel):
    """用户注册模型"""
    name: str  # 角色
    permissions: list  # 确认密码


class RoleUpdateSchema(BaseModel):
    """用户注册模型"""
    id: int  # 角色
    name: str  # 角色
    permissions: list  # 确认密码
