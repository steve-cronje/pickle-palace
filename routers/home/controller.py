from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from db import database, crud, schemas

router = APIRouter(tags=['home'])

templates = Jinja2Templates("templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("home/index.html", {'request': request})


@router.get("/form", response_class=HTMLResponse, name='form-get')
def get_form(request: Request, db: Session = Depends(database.get_db)):
    user_list = crud.get_users(db)
    return templates.TemplateResponse("forms/user.html", {"request": request, "user_list": user_list})


@router.post("/form", response_class=HTMLResponse, name='form-post')
def post_form(username: Annotated[str, Form()], 
              email: Annotated[str, Form()], 
              password: Annotated[str, Form()], 
              db: Session = Depends(database.get_db)):
    
    print(f"username: {username}\npassword: {password}\nemail: {email}\n")
    db_user = crud.get_user_by_email(db, email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = schemas.UserCreate(username=username, email=email, password=password)
    new_user = crud.create_user(db, user)
    print(new_user)
    return RedirectResponse('/form', status_code=status.HTTP_302_FOUND)