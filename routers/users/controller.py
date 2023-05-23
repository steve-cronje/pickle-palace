from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, UploadFile, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from config.auth.util import create_access_token, get_password_hash
from db import database, crud
from dependencies.auth import get_current_active_user
from schemas.user import Token, User, UserInDb
from .util import save_upload_file


from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_SECONDS
from db.crud import authenticate_user



router = APIRouter(tags=['user'], prefix='/user')
templates = Jinja2Templates('templates')


@router.get("/token", response_class=HTMLResponse, name='login')
def get_token(request: Request):
    return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/token", response_class=RedirectResponse, name='login')
def login_for_access_token(
                            db: Annotated[Session, Depends(database.get_db)], 
                           form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(router.url_path_for('get_me'), status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='authorization', value=access_token, httponly=True)
    # token = Token(access_token=access_token, token_type="bearer")
    return response


@router.get("/me", response_class=HTMLResponse, name='get_me')
def read_users_me(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user:
        return templates.TemplateResponse('users/user.html', {'request': request, 'user': current_user})
    else:
        raise HTTPException(401, 'Unauthorized')


@router.post("/me/edit", response_class=HTMLResponse, name='edit_user')
def edit_user(response: Response, 
              current_user: Annotated[User, Depends(get_current_active_user)],
              db: Annotated[Session, Depends(database.get_db)], 
              fullname: Annotated[str | None, Form()], 
              image: UploadFile):
    
    user_image = save_upload_file(image, current_user.username)
    crud.edit_user(db, current_user.id, fullname, user_image)
    return RedirectResponse(router.url_path_for('get_me'), status_code=status.HTTP_302_FOUND)


@router.get("/me/edit", response_class=HTMLResponse, name='edit_game')
def get_edit_user(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    return templates.TemplateResponse('users/edit.html', {'request': request, 'current_user': current_user})


@router.get("/signup", response_class=HTMLResponse, name='signup')
def get_signup(request: Request):
    return templates.TemplateResponse("users/signup.html", {'request': request})


@router.post("/signup", response_model=User, name='signup')
def post_signup(db: Annotated[Session, Depends(database.get_db)], 
                username: Annotated[str, Form()], 
                email: Annotated[str, Form()],
                password: Annotated[str, Form()]):
    
    user = UserInDb(username=username, email=email, password=get_password_hash(password))
    if crud.create_user(db, user):
        return user
    



@router.get("/logout", response_class=HTMLResponse, name='logout')
def get_logout(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    return templates.TemplateResponse('users/logout.html', {'request': request, 'user': current_user})

@router.post("/logout", response_class=HTMLResponse, name='logout')
def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='authorization', httponly=True)
    return response


@router.get("/delete_token", response_class=HTMLResponse, name='delete_token')
def get_delete_token(request: Request):
    return templates.TemplateResponse('users/delete_token.html', {'request': request})


@router.post("/delete_token", response_class=HTMLResponse, name='delete_token')
def logout(response: Response):
    response.delete_cookie(key='authorization', httponly=True)
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/{user_id}", response_class=HTMLResponse, name='user')
def get_user(request: Request, db: Annotated[Session, Depends(database.get_db)], user_id: int):
    user = crud.get_user(db, user_id)
    return templates.TemplateResponse('users/user.html', {'request': request, 'user': user})

    
