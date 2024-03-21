# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：v1.py
@IDE：PyCharm
@Description：导航视图
"""
from fastapi import APIRouter
from api.auth import views as auth_views
from api.user import views as user_views
from api.role import views as role_views
from api.log import views as log_views


class ApiRouter(object):
    """
    注册路由
    """

    def __new__(cls, *args, **kwargs):
        router = APIRouter()
        router.include_router(user_views.router, prefix="/api/user", tags=["User"])
        router.include_router(auth_views.router, prefix="/api", tags=["Auth"])
        router.include_router(role_views.router, prefix="/api/role", tags=["Role"])
        router.include_router(log_views.router, prefix="/api/log", tags=["Log"])
        return router
