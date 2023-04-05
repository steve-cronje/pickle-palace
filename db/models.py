from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class Pickle(Base):
    __tablename__ = "pickles"

    name = Column(String, primary_key=True)
    colour = Column(String)
    taste = Column(String)