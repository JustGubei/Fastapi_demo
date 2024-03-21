# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：LoggerMid.py
@IDE：PyCharm
@Description：中间件
"""

from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from core.middlerwares.AuthorizationMid import AuthorizationMiddleware
from core.middlerwares.LoggerMid import LoggerMiddleware
from env import setting

middleware = [
    # 跨域中间件
    Middleware(CORSMiddleware, allow_origins=setting.CORS_ORIGINS, allow_credentials=setting.CORS_ALLOW_CREDENTIALS,
               allow_methods=setting.CORS_ALLOW_METHODS, allow_headers=setting.CORS_ALLOW_HEADERS),
    # 日志中间件
    Middleware(AuthorizationMiddleware),
    # 认证中间件
    Middleware(LoggerMiddleware),
]
