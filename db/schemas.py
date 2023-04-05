from pydantic import BaseModel


class PickleBase(BaseModel):
    name: str
    colour: str
    taste: str


class PickleCreate(PickleBase):
    pass


class Pickle(PickleBase):
    
    class Config:
        orm_mode = True
