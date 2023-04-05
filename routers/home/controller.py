from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from db import database, crud, schemas
from dependencies.auth import get_current_user

router = APIRouter(tags=['home'])

templates = Jinja2Templates("templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("home/index.html", {'request': request})


