# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:30
@Auth： gubei
@File：__init__.py
@IDE：PyCharm
@Description：
"""

from typing import Optional

import jwt

from datetime import timedelta, datetime
from fastapi import HTTPException, Request
from pydantic import ValidationError
from jwt import PyJWTError
from starlette.responses import JSONResponse

from api.user.models import User
from env import setting


def create_access_token(data: dict):
    """
    创建token
    :param data: 加密数据
    :return: jwt
    """
    token_data = data.copy()
    # token超时时间
    expire = datetime.utcnow() + timedelta(
        seconds=setting.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)  # minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    # 向jwt加入超时时间
    token_data.update({"exp": expire})
    # jwt加密
    jwt_token = jwt.encode(token_data, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)

    return jwt_token


async def check_token(request, token):
    """
    权限验证
    @param request:
    @param token:
    """
    # ----------------------------------------验证JWT token------------------------------------------------------------
    try:
        # token解密
        request.state.detail = ""
        payload = jwt.decode(
            token,
            setting.JWT_SECRET_KEY,
            algorithms=[setting.JWT_ALGORITHM]
        )
        print(token)
        print(payload)
        if payload:
            user_id = payload.get("user_id", None)
            user_name = payload.get("user_name", None)
            print(user_id, user_name)
            # 无效用户信息
            if user_id is None or user_name is None:
                raise HTTPException(status_code=400, detail={"detail": "Not authenticated"})
            else:
                # 缓存用户ID
                request.state.user_id = user_id
                # 缓存用户类型
                request.state.user_name = user_name
        else:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    except (PyJWTError, ValidationError):
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


async def get_current_user(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        user_id = payload.get("user_id", None)
        user = await get_user_by_id(user_id)
        return user
    except:
        return None


async def get_user_by_id(user_id: int) -> Optional[User | None]:
    # 用户ID查询用户身份信息
    if user_id:
        user = await User.filter(id=user_id).first()
    else:
        user = None
    return user


async def check_permissions(request: Request):
    """
    权限验证
    @param request:
    """
    # ----------------------------------------验证JWT token------------------------------------------------------------
    try:
        # token解密
        request.state.detail = ""
        token = request.headers.get("authorization")
        payload = jwt.decode(
            token,
            setting.JWT_SECRET_KEY,
            algorithms=[setting.JWT_ALGORITHM]
        )
        print(token)
        print(payload)
        if payload:
            user_id = payload.get("user_id", None)
            username = payload.get("username", None)
            print(user_id, username)
            # 无效用户信息
            if user_id is None or username is None:
                raise HTTPException(status_code=400, detail="无效凭证")
            else:
                # 缓存用户ID
                request.state.user_id = user_id
                # 缓存用户类型
                request.state.username = username

        else:
            raise HTTPException(status_code=401, detail="无效凭证")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="凭证已过期")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效凭证")

    except (PyJWTError, ValidationError):
        raise HTTPException(status_code=401, detail="无效凭证")

# print(create_access_token({"user_id": 1, "user_type": 1, "username": '李刚'}))
