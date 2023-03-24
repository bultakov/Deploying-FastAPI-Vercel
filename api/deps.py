from typing import Union, Any
from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .schemas import User, TokenData
from .utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)

users: dict = {
    "bultakov": {
        "username": "bultakov",
        "full_name": "Ibrohim Bultakov",
        "email": "bii23@gmail.com",
        "hashed_password": "$2b$12$Tw9sxhiI11.PlYyGBHq.Y.nyd6Dcx3MKam16Mx3xB2MlwJs5sjihO",
    }
}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(payload)
        token_data = TokenData(**payload)
        print(token_data)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=404,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=404,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: dict = users.get(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Could not find user",
        )

    return User(**user)
