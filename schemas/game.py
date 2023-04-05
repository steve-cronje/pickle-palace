from pydantic import BaseModel
from datetime import date


class GenreBase(BaseModel):
    name: str


class Genre(GenreBase):
    class Config:
        orm_mode = True


class ScreenshotBase(BaseModel):
    url: str


class Screenshot(ScreenshotBase):
    game_id: str

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    id: str
    my_review: str | None = None
    favourite: bool | None = None


class GameInDb(GameBase):
    pass


class Game(GameBase):
    name: str
    release_date: date
    description: str
    cover_url: str
    screenshots: list[Screenshot]
    genres: list[Genre]

    class Config:
        orm_mode = True
