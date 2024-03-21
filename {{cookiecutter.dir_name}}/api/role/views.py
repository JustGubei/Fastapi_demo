# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：views.py
@IDE：PyCharm
@Description：
"""

from fastapi import APIRouter, Depends, Query
from tortoise.transactions import in_transaction

from api.role.models import Role, Permission
from api.role.serializers import RoleCreateSchema, RoleUpdateSchema
from api.user.models import User
from core.auth.oauth2 import get_current_active_user
from core.models.response import *

router = APIRouter()


@router.get("/list", summary='获取角色列表')
async def get_roles(page: int = Query(1, alias="page"), pagesize: int = Query(10)):
    roles = await Role.filter().all().offset(page - 1).limit(pagesize)
    total_roles = await Role.all().count()
    return R.suc(data=roles, total=total_roles)


@router.post('', summary='添加角色并赋予权限')
async def add_role(roleCreate: RoleCreateSchema):
    async with in_transaction():
        # 使用 get_or_create 避免多次查询
        role, created = await Role.get_or_create(name=roleCreate.name)

        if not created:
            return R.err(msg="角色已存在")

        # 创建权限并与角色关联
        permissions = Permission(content=str(roleCreate.permissions))
        await permissions.save()
        role.permissions = permissions
        await role.save()

    return R.suc()


@router.put('', summary='修改角色权限')
async def add_role(roleUpdateSchema: RoleUpdateSchema):
    async with in_transaction():
        role = await Role.filter(id=roleUpdateSchema.id).first()
        role.name = roleUpdateSchema.name
        role.permissions.content = str(roleUpdateSchema.permissions)
        await role.save()

    return R.suc(msg="修改角色权限成功")


@router.delete("/{role_id}", summary='删除角色信息')
async def delete_role(role_id: int):
    role = await Role.get(id=role_id)
    role.is_delete = True
    role.permissions.is_delete = True
    await role.save()
    return R.suc(msg="角色删除成功")
