# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：serializers.py
@IDE：PyCharm
@Description：
"""

from enum import Enum
from typing import List

from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    """用户注册模型"""
    username: str = ""  # 角色
    nickname: str = ""  # 昵称
    password: str = ""  # 密码
    permissions: list


class UserUpdate(BaseModel):
    id: int
    nickname: str
    password: str
    role: int


class UserRole(str, Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []


class UserToken(BaseModel):
    id: int
    user_name: str
    nick_name: str
    disabled: bool
