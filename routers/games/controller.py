from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from db import database, crud
from schemas import game


router = APIRouter(prefix='/games', tags=['games'])
templates = Jinja2Templates('templates')


@router.get('/', response_class=HTMLResponse, name='games-list')
def games_list(request: Request, db: Annotated[Session, Depends(database.get_db)]):
    games = crud.get_games(db)
    return templates.TemplateResponse('games/list.html', {"request": request, "games": games})


@router.get("/new-game", response_class=HTMLResponse, name='new-game')
def new_game_form(request: Request):
    return templates.TemplateResponse('games/create-form.html', {"request": request})


@router.post("/new-game", response_class=HTMLResponse, name='new-game')
def new_game(game_id: Annotated[int, Form()], 
             my_review: Annotated[str, Form()],
             db: Annotated[Session, Depends(database.get_db)],
             favourite: bool = Form(False)):

    schema_game = game.GameInDb(id=game_id, my_review=my_review, favourite=favourite)
    db_game = crud.create_game(db, schema_game)
    return RedirectResponse(url=router.url_path_for('game', game_id=db_game.id), status_code=status.HTTP_302_FOUND)


@router.get("/{game_id}", response_class=HTMLResponse, name='game')
def view_game(request: Request, game_id: int, db: Annotated[Session, Depends(database.get_db)]):
    db_game = crud.get_game(db, game_id)
    return templates.TemplateResponse('games/game.html', {"request": request, "game": db_game})


@router.get("/{game_id}/delete", response_class=HTMLResponse, name='delete-game')
def delete_game_form(request: Request, game_id: int, db: Annotated[Session, Depends(database.get_db)]):
    db_game = crud.get_game(db, game_id)
    return templates.TemplateResponse('games/delete-form.html', {"request": request, "game": db_game})


@router.post("/{game_id}/delete", response_class=HTMLResponse, name='delete-game')
def delete_game(game_id: int, db: Annotated[Session, Depends(database.get_db)]):
    db_game = crud.get_game(db, game_id)
    crud.delete_game(db, db_game)
    return RedirectResponse(router.url_path_for('games-list'), status_code=status.HTTP_302_FOUND)

