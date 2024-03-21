# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：__init.py
@IDE：PyCharm
@Description：loguru日志的封装类，导入即可直接使用
"""

from functools import wraps

import loguru
from fastapi import Request, Depends

from env import setting


def set_request_action(request: Request, action: str, ) -> None:
    """先定义一个设置 action 的辅助函数，后续想到优化方案再说"""
    request.scope['action'] = action


# 单例类的装饰器
def singleton_class_decorator(cls):
    """
    装饰器，单例类的装饰器
    """
    # 在装饰器里定义一个字典，用来存放类的实例。
    _instance = {}

    # 装饰器，被装饰的类
    @wraps(cls)
    def wrapper_class(*args, **kwargs):
        # 判断，类实例不在类实例的字典里，就重新创建类实例
        if cls not in _instance:
            # 将新创建的类实例，存入到实例字典中
            _instance[cls] = cls(*args, **kwargs)
        # 如果实例字典中，存在类实例，直接取出返回类实例
        return _instance[cls]

    # 返回，装饰器中，被装饰的类函数
    return wrapper_class


@singleton_class_decorator
class Logger:
    def __init__(self):
        self.logger_add()

    @staticmethod
    def logger_add():
        loguru.logger.add(
            # 水槽，分流器，可以用来输入路径
            sink=setting.LOG_PATH,
            # 日志等级
            level=setting.LOG_LEVEL,
            # 日志创建周期
            rotation=setting.ROTATION,
            # 保存
            retention=setting.RETENTION,
            # 文件的压缩格式
            compression=setting.COMPRESSION,
            # 编码格式
            encoding="utf-8",
            # 具有使日志记录调用非阻塞的优点
            enqueue=True
        )

        if not setting.LOG_IS_WRITE_TO_CONSOLE:
            loguru.logger.remove(handler_id=0)
        if not setting.LOG_IS_WRITE_TO_FILE:
            loguru.logger.remove(handler_id=1)



    @property
    def get_logger(self):
        return loguru.logger


'''
# 实例化日志类
'''
logger = Logger().get_logger
