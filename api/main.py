from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from .deps import get_current_user, users
from .schemas import User
from .utils import verify_password, create_access_token, create_refresh_token, get_hashed_password

app = FastAPI(docs_url='/docs', redoc_url=None)


class UserAuth(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str


@app.get('/')
async def home():
    return {
        "docs_url": "https://deploying-fastapi-vercel.vercel.app/docs/"
    }


@app.post('/signup', response_model=User)
async def create_user(data: UserAuth):
    user = users.get(data.username)
    if user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'username': data.username,
        'full_name': data.full_name,
        'email': data.email,
        'hashed_password': get_hashed_password(password=data.hashed_password),
    }
    users[data.username] = user
    return user


@app.post('/token')
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)
    if user is None:
        return {
            "success": "error",
            "message": "Foydalanuvchi topilmadi!!!"
        }

    hashed_pass = user.get('hashed_password')
    if not verify_password(form_data.password, hashed_pass):
        return {
            "success": "error",
            "message": "Foydalanuvchi paroli xato!!!"
        }
    access_token: str = create_access_token(form_data.username)
    refresh_token: str = create_refresh_token(form_data.username)
    return {
        "success": "ok",
        "data": {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }


@app.get('/me', response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    return user
