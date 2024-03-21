# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：mysqldb.py
@IDE：PyCharm
@Description： 暂时未用到
"""

from core.log import logger
from utils.sql_tool import make_find_sql, make_insert_sql, make_update_sql
from env import setting
from typing import List, Any
import aiomysql
import datetime
import json


class MysqlDB:
    def __init__(
            self, ip=None, port=None, db=None, user_name=None, user_pass=None, **kwargs
    ):
        # 可能会改setting中的值，所以此处不能直接赋值为默认值，需要后加载赋值
        self.connect_pool = None
        if not ip:
            self.ip = setting.MYSQL_IP
        if not port:
            self.port = setting.MYSQL_PORT
        if not db:
            self.db = setting.MYSQL_DB
        if not user_name:
            self.user_name = setting.MYSQL_USER_NAME
        if not user_pass:
            self.user_pass = setting.MYSQL_USER_PASS

    async def get_connection_pool(self):
        try:
            self.connect_pool = await aiomysql.create_pool(
                host=self.ip,
                port=self.port,
                user=self.user_name,
                password=self.user_pass,
                db=self.db,
                minsize=1,
                maxsize=10,
                echo=True,
                autocommit=True,
            )
        except Exception as e:
            logger.error(
                """
            连接数据失败：
            ip: {}
            port: {}
            db: {}
            user_name: {}
            user_pass: {}
            exception: {}
            """.format(
                    self.ip, self.port, self.db, self.user_name, self.user_pass, e
                )
            )

    async def find(
            self,
            table_name: str,
            columns: List,
            condition: Any,
            limit: int = 0,
            to_json: bool = True,
    ):
        """
        @summary: 条件查询表
        ---------
        @ param table_name: 表名
        @ param columns: 待查询列名
        @ param condition: 查询条件
        @ param limit: == 1 返回个数为1 else 全部
        @ param to_json: 是否返回字典格式
        ---------
        @result: 添加行数
        """
        async with self.connect_pool.acquire() as conn:
            async with conn.cursor() as cur:
                count = await cur.execute(make_find_sql(table=table_name, columns=columns, condition=condition))
                if not count:
                    return None
                if not limit:
                    results = await cur.fetchall()
                else:
                    results = await cur.fetchone()
                if to_json:
                    columns = [i[0] for i in cur.description]

                    def convert(col):
                        if isinstance(col, (datetime.date, datetime.time)):
                            return str(col)
                        elif isinstance(col, str) and (
                                col.startswith("{") or col.startswith("[")
                        ):
                            try:
                                # col = self.unescape_string(col)
                                return json.loads(col)
                            except:
                                return col
                        else:
                            # col = self.unescape_string(col)
                            return col

                    if limit == 1:
                        results = [convert(col) for col in results]
                        results = dict(zip(columns, results))
                    else:
                        results = [[convert(col) for col in row] for row in results]
                        results = [dict(zip(columns, r)) for r in results]
                return results

    async def add(
            self,
            sql,
            exception_callfunc=None
    ):
        """
        sql插入数据
        Args:
            sql:
            exception_callfunc: 异常回调
        Returns: 添加行数
        """
        affect_count = 0
        async with self.connect_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    affect_count = cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    exception_callfunc(e)
                pass
            return affect_count

    async def add_smart(
            self,
            table,
            data: dict,
            **kwargs
    ):
        """
        sql插入数据
        Args:
            table: 表名
            data: 字典 {"xxx":"xxx"}
            kwargs： auto_update=False, update_columns=(), insert_ignore=False
        Returns: 添加行数
        """
        sql = make_insert_sql(table=table, data=data, **kwargs)
        return self.add(sql)

    async def update(
            self,
            sql
    ):
        """
        sql更新数据
        Args:
            sql: 表名
        """
        async with self.connect_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    cur.execute(sql)
                except Exception as e:
                    logger.error(e)

    async def update_smart(
            self,
            table,
            data: dict,
            condition: str
    ):
        """
        更新
        Args:
            table: 表名
            data: 数据 {"xxx":"xxx"} 需要更新的ke-value
            condition: 条件
        """
        sql = make_update_sql(table, data, condition)
        return self.update(sql)

    async def init_mysql(self):
        await self.get_connection_pool()

    async def close_mysql(self):
        self.connect_pool.close()


mysql = MysqlDB()
