# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：LoggerMid.py
@IDE：PyCharm
@Description：日志中间件，用于写日志到mysql数据库
"""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from core.log import logger
from env import setting
from utils.log_to_mysql import write_to_database
from core.auth import get_current_user


class LoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        start_time = int(time.time() * 1000)
        response = await call_next(request)
        end_time = int(time.time() * 1000)

        token = request.headers.get("authorization", None)

        current_user = await get_current_user(token[7:]) if token else ''
        log_record = {"user": current_user.user_name if current_user else '',
                      "api": request.url.path,
                      "method": request.method,
                      "status_code": response.status_code, "action": request.scope.get('action', ''),
                      "ip": request.client.host,
                      "response_time": "{:.2f}s".format((end_time - start_time) / 1000)}

        if setting.LOG_IS_WRITE_TO_MYSQL:
            await write_to_database(log_record)

        logger.info(
            f"请求:{request.method} | {request.url.path} | {request.client.host} | 响应:{response.status_code} | "
            f"耗时: {(end_time - start_time) / 1000}s", extra=log_record)

        return response
