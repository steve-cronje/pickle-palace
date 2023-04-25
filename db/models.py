from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base



class Pickle(Base):
    __tablename__ = "pickles"

    name = Column(String, primary_key=True)
    colour = Column(String)
    taste = Column(String)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    release_date = Column(Date)
    description = Column(String)
    my_review = Column(String)
    cover_url = Column(String)
    favourite = Column(Boolean)
    screenshots = relationship('GameScreenshot', cascade="all, delete-orphan")
    genres = relationship('GameGenre', secondary='game_genres_association', back_populates='games')

class GameGenre(Base):
    __tablename__ = "game_genres"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship('Game', secondary='game_genres_association', back_populates='genres')


class GameGenreAssociation(Base):
    __tablename__ = "game_genres_association"

    id = Column(Integer, primary_key=True, index=True)
    notes = Column(String, nullable=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    genre_id = Column(Integer, ForeignKey('game_genres.id'))

class GameScreenshot(Base):
    __tablename__ = "game_screenshots"

    url = Column(String, primary_key=True)
    game_id = Column(ForeignKey(Game.id))



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    image = Column(String, nullable=True)
    date_joined = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
