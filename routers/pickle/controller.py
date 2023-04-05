from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from db import database, crud
from schemas import pickle

router = APIRouter(tags=['pickle'], prefix='/pickle')

templates = Jinja2Templates("templates")

@router.get('/pickles', response_class=HTMLResponse, name='pickle-list')
def list_pickles(request: Request, db: Annotated[Session, Depends(database.get_db)]):
    pickle_list = crud.get_pickles(db)
    return templates.TemplateResponse('pickle/list.html', {"request": request, 'pickle_list': pickle_list})


@router.get('/create', response_class=HTMLResponse, name='pickle-create-form')
def create_pickle_form(request: Request):
    return templates.TemplateResponse('pickle/form.html', {"request": request})


@router.post('/create', response_class=HTMLResponse, name='pickle-create')
def create_pickle(name: Annotated[str, Form()],
                colour: Annotated[str, Form()], 
                taste: Annotated[str, Form()], 
                db: Annotated[Session, Depends(database.get_db)]):
    
    db_pickle = crud.get_pickle(db, name)
    
    if db_pickle: 
        raise HTTPException(status_code=400, detail="Pickle already exists!")
    
    schema_pickle = pickle.PickleCreate(name=name, colour=colour, taste=taste)
    pickle = crud.create_pickle(db, schema_pickle)
    return RedirectResponse(f'/pickle/{pickle.name}', status_code=status.HTTP_302_FOUND)


@router.get('/{pickle_name}', response_class=HTMLResponse, name='pickle')
def view_pickle(pickle_name: str, request: Request, db: Annotated[Session, Depends(database.get_db)]):
    pickle = crud.get_pickle(db, pickle_name)
    return templates.TemplateResponse('pickle/pickle.html', {"request": request, 'pickle': pickle})


@router.get('/{pickle_name}/delete', response_class=HTMLResponse, name='pickle-delete-confirm')
def delete_pickle_confirm(pickle_name: str, request: Request, db: Annotated[Session, Depends(database.get_db)]):
    pickle = crud.get_pickle(db, pickle_name)
    return templates.TemplateResponse('pickle/delete.html', {"request": request, 'pickle': pickle})


@router.post('/{pickle_name}/delete', response_class=HTMLResponse, name='pickle-delete')
def delete_pickle(pickle_name: str, db: Annotated[Session, Depends(database.get_db)]):
    pickle = crud.get_pickle(db, pickle_name)
    crud.delete_pickle(db, pickle)
    return RedirectResponse('/pickle/pickles', status_code=status.HTTP_302_FOUND)
