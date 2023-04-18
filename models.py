from sqlalchemy import Column, String, Integer
from database import Base


class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key = True)
    task = Column(String(256))