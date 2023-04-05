from sqlalchemy.orm import Session

from db import models, schemas


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
    
    