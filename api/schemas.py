from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    exp: int
    sub: str


class User(BaseModel):
    username: str
    email: str
    full_name: str


class UserInDB(User):
    password: str


class UserAuth(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
