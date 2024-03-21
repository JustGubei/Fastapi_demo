# -*- coding: utf-8 -*-
import base64
import hashlib


# 加密
def get_md5(*args):
    """
    @summary: 获取唯一的32位md5
    """

    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_sha1(*args):
    """
    @summary: 获取唯一的40位值， 用于获取唯一的id
    """

    sha1 = hashlib.sha1()
    for arg in args:
        sha1.update(str(arg).encode())
    return sha1.hexdigest()  # 40位


def get_base64(data):
    if data is None:
        return data
    return base64.b64encode(str(data).encode()).decode("utf8")


def key2hump(key):
    """
    下划线试变成首字母大写
    """
    return key.title().replace("_", "")