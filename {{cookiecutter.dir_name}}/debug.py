# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File： debug.py
@IDE：PyCharm
@Description：windows启动文件
"""
from core.init import InitializeApp
import uvicorn

from env import setting

app = InitializeApp()

if __name__ == "__main__":
    uvicorn.run(
        app='debug:app',
        host=setting.APP_HOST,
        port=setting.APP_PORT,
        reload=True,
        # log_level="critical"
    )
