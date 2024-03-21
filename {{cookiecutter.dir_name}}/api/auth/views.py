# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：views.py
@IDE：PyCharm
@Description：
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core.auth.oauth2 import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/token", summary='获取token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"user_id": user.id, "user_name": user.user_name},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
