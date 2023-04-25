from pydantic import BaseModel, EmailStr, FileUrl
from datetime import datetime


class UserBase(BaseModel):

    username: str
    email: EmailStr


class UserInDb(UserBase):

    password: str


class User(UserBase):

    id: int
    is_active: bool
    date_joined: datetime
    full_name: str | None = None
    image: FileUrl | None = None

    class Config:

        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None