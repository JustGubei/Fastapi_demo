# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：timmer.py
@IDE：PyCharm
@Description：定时器
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.log import logger


def demo():
    logger.info("开启定时任务......")

    pass
    # logger.info("开启定时任务......")


scheduler = AsyncIOScheduler()
# scheduler.add_job(func=demo, trigger='interval', hours=1)

