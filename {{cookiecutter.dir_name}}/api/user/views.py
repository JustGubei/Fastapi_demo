# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：views.py
@IDE：PyCharm
@Description：
"""

from fastapi import APIRouter, Depends, Request, Query
from tortoise.functions import Count
from tortoise.queryset import QuerySet

from api.user.models import User
from api.user.serializers import UserRegisterSchema, UserToken, UserUpdate
from core.auth.oauth2 import get_current_active_user, get_password_hash
from core.log import set_request_action
from core.models.response import *

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/me/", summary='获取当前用户信息')
async def read_users_me(request: Request):
    set_request_action(request, action=f"查看了{request.state.current_user.user_name}用户信息")
    return R.suc()


@router.get("/user/{user_id}", summary='根据ID获取用户信息')
async def read_user(user_id: int):
    user = await User.filter(id=user_id).first()
    return R.suc(data=user)


@router.get("/users", summary='获取所有用户信息')
async def read_users(page: int = Query(1, alias="page"), pagesize: int = Query(10)):
    users = await User.all().offset(page - 1).limit(pagesize)
    total_users = await User.all().count()
    # 一次性获取总用户数和分页数据
    return R.suc(data=users, total=total_users)


@router.post('/user', summary='新增用户信息')
async def add_user(request: Request, register: UserRegisterSchema):
    """用户注册"""

    db_user = await User.filter(user_name=register.username).first()
    if db_user:
        return R.err(msg="用户已存在")

    password = get_password_hash(register.password)

    # 创建一个新的用户，并关联指定的角色
    new_user = User()
    new_user.user_name = register.username
    new_user.nick_name = register.nickname
    new_user.user_pwd = password
    new_user.permissions = str(register.permissions)
    await new_user.save()

    set_request_action(request, f"新建了{register.username}用户")
    return R.suc(msg='用户创建成功')


@router.put("/user/status", summary='更新用户状态')
async def update_user_status(user_id: int):
    user = await User.filter(id=user_id).first()
    user.disabled = not user.disabled
    await user.save()
    return R.suc(msg='用户状态更新成功')


@router.put("/user/pwd", summary='修改用户密码')
async def update_user_pwd(user_id: int, password: str):
    user = await User.filter(id=user_id).first()
    user.user_pwd = password
    await user.save()
    return R.suc(msg='用户密码更新成功')


@router.put("/user/role", summary='修改用户角色')
async def update_user_pwd(user_id: int, role_id: str):
    if current_user.role != 0:
        return R.err(msg='无权限操作')
    user = await User.filter(id=user_id).first()
    user.role_id = role_id
    await user.save()
    return R.suc(msg='用户角色更新成功')
