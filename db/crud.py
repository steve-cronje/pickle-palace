from sqlalchemy.orm import Session

from db import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_pickles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pickle).offset(skip).limit(limit).all()


def get_pickle(db:Session, name: str):
    return db.query(models.Pickle).filter(models.Pickle.name == name).first()


def create_pickle(db: Session, item: schemas.PickleCreate):
    db_pickle = models.Pickle(name=item.name, colour=item.colour, taste=item.taste)
    db.add(db_pickle)
    db.commit()
    db.refresh(db_pickle)
    return db_pickle


def delete_pickle(db: Session, del_obj: schemas.Pickle):
    db_pickle = db.query(models.Pickle).filter(models.Pickle.name == del_obj.name).first()
    db.delete(db_pickle)
    db.commit()
    
    