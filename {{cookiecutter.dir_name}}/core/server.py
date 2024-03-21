# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File： init.py
@IDE：PyCharm
@Description：服务器初始化项目
"""
from tortoise.contrib.fastapi import register_tortoise
from core.db.ormdb import TORTOISE_ORM
from fastapi import FastAPI
from pathlib import Path as PyPath
from core.log import logger
from core.middlerwares.middleware import middleware
from core.timer import scheduler
from core.router import v1
from utils.get_local_ip import local_ip
from utils.use_loacl_static import use_local_static
from env import setting


class InitializeApp(object):
    """
    注册App
    """

    current_project_path = PyPath(__file__).resolve().parent.parent  # 获取当前项目根目录路径
    static_templates_path = current_project_path / "templates" / "static"  # 拼接路径

    def __new__(cls, *args, **kwargs):
        app = FastAPI(title=setting.APP_TITLE, description=setting.APP_DESCRIPTION,middleware=middleware)
        cls.event_init(app)
        cls.register_router(app)
        return app

    @staticmethod
    def register_router(app: FastAPI) -> None:
        """
        注册路由
        :param app:
        :return:
        """
        # 项目API
        app.include_router(
            v1.ApiRouter(),
        )

    @staticmethod
    def event_init(app: FastAPI) -> None:
        """
        事件初始化
        :param app:
        :return:
        """

        @app.on_event("startup")
        async def startup():
            # 屏蔽警告
            warnings.filterwarnings("ignore", category=Warning)

            # 使用本地静态资源
            use_local_static()

            register_tortoise(
                app,
                config=TORTOISE_ORM,
                generate_schemas=True,  # 重启服务时自动生成数据库表；关闭，改为使用aerich
                add_exception_handlers=True,
            )
            scheduler.start()  # 定时任务
            logger.info(f"项目启动成功，文档地址：http://{setting.APP_HOST}:{setting.APP_PORT}/docs")
            pass

        @app.on_event('shutdown')
        async def shutdown():
            """
            关闭
            :return:
            """
            # await mysql.close_mysql()
            scheduler.shutdown()
