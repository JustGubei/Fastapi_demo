# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：response.py
@IDE：PyCharm
@Description：响应类
"""

from typing import Any, T


class R(object):

    @staticmethod
    def suc(data: T = None, msg: str = "SUCCESS", total: T = None, code: int = 200):
        content = {
            'code': code,
            'msg': msg,
        }
        if data is not None:
            content['data'] = data
        if total:
            content['total'] = total
        return content

    @staticmethod
    def err(data: str = None, msg: str = "BAD REQUEST", code: int = 400):
        content = {
            'code': code,
            'msg': msg,
        }
        if data is not None:
            content['data'] = data
        return content
