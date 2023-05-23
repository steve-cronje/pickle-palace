from sqlalchemy.orm import Session
from db import models
from schemas import pickle, game, user
from api.igdb.util import get_igdb_game, get_screenshots_for_game
from config.auth.util import verify_password


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


def edit_game(db: Session, game_id, my_review, favourite):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    game.my_review = my_review
    game.favourite = favourite
    db.commit()
    db.refresh(game)
    return game


def delete_game(db: Session, game: game.Game):
    db_game = db.query(models.Game).filter(models.Game.id == game.id).first()
    db.delete(db_game)
    db.commit()


# //////// USER AUTH ///////////


def get_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user


def get_user_by_email(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user


def get_user(db: Session, id: int):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    return db_user


def create_user(db: Session, user: user.UserInDb):
    if db.query(models.User).filter(models.User.username == user.username).first() is None:
        db_user = models.User(username=user.username,
                            email=user.email,
                            password=user.password)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None
    

def edit_user(db: Session, user_id: int, full_name: str | None = None, image: str | None = None):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    print(full_name)
    print(image)
    if full_name is not None:
        db_user.full_name = full_name
    if image is not None:
        db_user.image = image

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: user.User):

    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db.delete(db_user)
    db.commit()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
