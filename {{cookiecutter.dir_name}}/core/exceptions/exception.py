# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：exception.py
@IDE：PyCharm
@Description：框架异常类，暂时不用
"""


class AuthenticationError(Exception):
    """
    未认证
    """

    def __init__(self, message: str = "Unauthorized"):
        self.message = message


class AuthorizationError(Exception):
    """
    未授权
    """

    def __init__(self, message: str = "Forbidden"):
        self.message = message