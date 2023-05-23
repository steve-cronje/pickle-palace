from typing import Annotated
from fastapi import Depends, status, Cookie, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from schemas.user import TokenData, User
from jose import jwt, JWTError
from config.config import AUTH_SECRET_KEY, ALGORITHM
from db import database
from db.crud import get_user_by_username
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_current_user(db: Annotated[Session, Depends(database.get_db)], 
                     authorization: str | None = Cookie(default=None)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if authorization is not None:
        try:
            payload = jwt.decode(authorization, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = get_user_by_username(db=db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    else:
        return None


def get_current_active_user(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    if current_user:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    return None
