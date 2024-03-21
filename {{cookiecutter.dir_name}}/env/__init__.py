# -*- coding: utf-8 -*-
"""
Created on 2023-09-22 17:05
---------
@summary: 爬虫入口
---------
@author: pepsi
"""
import platform

if platform.system() == "Windows":
    from .debug import Setting
else:
    from .release import Setting

setting = Setting()
