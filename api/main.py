from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import users_router

app = FastAPI(docs_url='/docs', redoc_url=None, debug=False)

app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)