from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


@app.get('/')
async def home():
    return {
        "docs_url": "https://deploying-fastapi-vercel.vercel.app/docs/"
    }
