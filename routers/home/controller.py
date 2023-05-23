from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from schemas.user import User
from dependencies.auth import get_current_active_user

router = APIRouter(tags=['home'])
templates = Jinja2Templates("templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    print(current_user)
    return templates.TemplateResponse("home/index.html", {'request': request, 'current_user': current_user})


