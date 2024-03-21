# -*- coding: utf-8 -*-
"""
@Time： 2023/12/20 16:20
@Auth： gubei
@File：mysqldb.py
@IDE：PyCharm
@Description：
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.user.models import User
from api.user.serializers import UserInDB, TokenData

security = HTTPBearer()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_user_in_db(username: str):
    user = await User.filter(user_name=username).first()
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user_in_db(username=username)
    if not user:
        return False

    if not verify_password(password, user.user_pwd):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": 401, "msg": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id", None)
        username = payload.get("user_name", None)
        print(username)
        # 无效用户信息
        if user_id is None or username is None:
            raise HTTPException(status_code=400, detail="无效用户信息", headers={"WWW-Authenticate": "Bearer"})
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    else:
        user = await get_user_in_db(str(username))
        if user is None:
            raise credentials_exception
        return user


async def get_current_user_mid(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": 401, "msg": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token[7:], SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id", None)
        username = payload.get("user_name", None)
        # 无效用户信息
        if user_id is None or username is None:
            raise HTTPException(status_code=400, detail="无效用户信息", headers={"WWW-Authenticate": "Bearer"})
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    else:
        user = await get_user_in_db(str(username))
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
