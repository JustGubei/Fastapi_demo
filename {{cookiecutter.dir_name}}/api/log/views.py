# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：views.py
@IDE：PyCharm
@Description：
"""

from fastapi import APIRouter, Query

from api.log.models import Logs
from core.models.response import *

router = APIRouter()


@router.get("s", summary='获取日志列表')
async def get_logs(page: int = Query(1, alias="page"), pagesize: int = Query(10)):
    logs = await Logs.filter().all().offset(page - 1).limit(pagesize)
    total_logs = await Logs.all().count()
    return R.suc(data=[i.to_dict() for i in logs], total=total_logs)

