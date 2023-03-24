from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(docs_url='/docs', redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserAuth(BaseModel):
    username: str
    full_name: str
    email: str
    password: str


@app.get('/')
async def home():
    return {
        "docs_url": "https://deploying-fastapi-vercel.vercel.app/docs/"
    }
