# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File： init.py
@IDE：PyCharm
@Description：windows下配置文件
"""
import os
from datetime import date
from typing import List
from pydantic import BaseSettings


class Setting(BaseSettings):
    # APP信息
    APP_TITLE: str = "这是项目标题"
    APP_DESCRIPTION : str = "这是项目描述"
    APP_MODE: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 10161
    APP_VERSION: str = "/v1"

    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # Session
    SECRET_KEY = "session"
    SESSION_COOKIE = "session_id"
    SESSION_MAX_AGE = 14 * 24 * 60 * 60

    # Jwt
    JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

    SWAGGER_UI_OAUTH2_REDIRECT_URL = "/api/v1/test/oath2"

    # 二维码过期时间
    QRCODE_EXPIRE = 60 * 1

    # 日志配置
    LOG_PATH = f'logs/{date.today()}.log'  # log存储路径
    LOG_LEVEL = "DEBUG"
    LOG_IS_WRITE_TO_CONSOLE = True  # 是否打印到控制台
    LOG_IS_WRITE_TO_FILE = False  # 是否写文件
    LOG_IS_WRITE_TO_MYSQL = True  # 是否写数据库
    ROTATION = "00:00"  # 日志切割时间
    COMPRESSION = 'zip'  # 日志压缩方式
    RETENTION = '7 days'  # 日志保留时间
    CATCH = True  # 捕获异常

    # 数据库配置
    MYSQL_IP = "172.18.2.198"
    MYSQL_PORT = 3306
    MYSQL_DB = "fastapi"
    MYSQL_USER_NAME = "root"
    MYSQL_USER_PASS = "root"
    MYSQL_DB_URL = f'mysql://{MYSQL_USER_NAME}:{MYSQL_USER_PASS}@{MYSQL_IP}:{MYSQL_PORT}/{MYSQL_DB}'
    MODELS_PATH: list = ['api.log.models', 'api.user.models', 'api.role.models']

    # 代理
    IP_AGENTS = [""]
