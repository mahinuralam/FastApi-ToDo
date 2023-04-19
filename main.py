from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import models
import schemas
from database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        

@app.get('/')
def root():
    return "todo"


@app.post('/todo', response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):
    
    todo = models.ToDo(task = todo.task)
    session.add(todo)
    session.commit()
    id = todo.id
    session.refresh(todo)
    session.close()
    
    return todo


@app.get('/todo/{id}', response_model=schemas.ToDo)
def get_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    session.close()
    if not todo:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return todo


@app.put('/todo/{id}', response_model=schemas.ToDo)
def update_todo(id: int, todo: schemas.ToDoCreate, session: Session = Depends(get_session)):
    get_db_data = session.query(models.ToDo).get(id)
    if get_db_data:
        get_db_data.task = todo.task
        session.commit()
    session.close()
    if not get_db_data:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return get_db_data


@app.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    if todo:
        session.delete(todo)
        session.commit()
    session.close()
    if not todo:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return None


@app.get('/todo', response_model = List[schemas.ToDo])
def read_todo_list(session: Session = Depends(get_session)):
    todo_list = session.query(models.ToDo).all()
    session.close()
    return todo_list