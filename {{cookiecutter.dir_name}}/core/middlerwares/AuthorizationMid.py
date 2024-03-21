# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：AuthorizationMid.py
@IDE：PyCharm
@Description：身份验证中间件
"""

import re

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


class AuthorizationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 不进行身份校验的接口地址
        excluded_paths = ["/docs", "/openapi.json", "/redoc", "/api/token", "/api/user/login", "/api/user/register",
                          "/api/user/forget"]

        for excluded_path in excluded_paths:
            if re.match(excluded_path, request.url.path):
                return await call_next(request)

        return await call_next(request)
