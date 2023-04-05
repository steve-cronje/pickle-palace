from sqlalchemy.orm import Session

from db import models
from schemas import pickle, game
from api.igdb.util import get_igdb_game, get_screenshots_for_game


def get_pickles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pickle).offset(skip).limit(limit).all()


def get_pickle(db:Session, name: str):
    return db.query(models.Pickle).filter(models.Pickle.name == name).first()


def create_pickle(db: Session, item: pickle.PickleInDb):
    db_pickle = models.Pickle(name=item.name, colour=item.colour, taste=item.taste)
    db.add(db_pickle)
    db.commit()
    db.refresh(db_pickle)
    return db_pickle


def delete_pickle(db: Session, del_obj: pickle.Pickle):
    db_pickle = db.query(models.Pickle).filter(models.Pickle.name == del_obj.name).first()
    db.delete(db_pickle)
    db.commit()
    

# //// Game Genres ////

def create_genres_from_list(db: Session, genre_list: list):
    db_list = []
    for genre in genre_list:
        genre_in_db = db.query(models.GameGenre).filter(models.GameGenre.name == genre).first()
        if genre_in_db:
            db_list.append(genre_in_db)
        else:
            db_genre = models.GameGenre(name=genre)
            db.add(db_genre)
            db.commit()
            db.refresh(db_genre)
            db_list.append(db_genre)
    return db_list


# //// Game Screenshots ////


def get_screenshots(db: Session, game_id: int):
    return db.query(models.GameScreenshot).filter(models.GameScreenshot.game_id == game_id).all()


def create_screenshots_from_list(db: Session, screenshot_list: list, game_id: int):
    print(screenshot_list)
    for screenshot in screenshot_list:
        screenshot_in_db = db.query(models.GameScreenshot).filter(models.GameScreenshot.url == screenshot).first()
        if screenshot_in_db:
            continue
        else: 
            db_screenshot = models.GameScreenshot(url=screenshot, game_id=game_id)
            db.add(db_screenshot)
            db.commit()
            db.refresh(db_screenshot)

    return get_screenshots(db, game_id)


# //// Games ////


def get_games(db: Session):
    return db.query(models.Game).all()


def get_game(db: Session, id: int):
    return db.query(models.Game).filter(models.Game.id == id).first()


def get_favourite_games(db: Session, favourite: bool):
    return db.query(models.Game).filter(models.Game.favourite == favourite).all()


def create_game(db: Session, game: game.GameInDb):
    game_dict = get_igdb_game(game_id=game.id)
    genre_list_db = create_genres_from_list(db, game_dict['genre_list'])
    game_db = models.Game(id=game.id, 
                          my_review=game.my_review, 
                          favourite=game.favourite, 
                          name=game_dict['name'],
                          release_date=game_dict['release_date'],
                          cover_url=game_dict['cover_url'],
                          description=game_dict['description'],
                          genres=genre_list_db)
    
    db.add(game_db)
    db.commit()
    screenshot_list_db = create_screenshots_from_list(db, get_screenshots_for_game(game.id), game.id)
    game_db.screenshots=screenshot_list_db
    db.commit()
    db.refresh(game_db)

    return game_db


def delete_game(db: Session, game: game.Game):
    db_game = db.query(models.Game).filter(models.Game.id == game.id).first()
    db.delete(db_game)
    db.commit()


