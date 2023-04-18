from fastapi import FastAPI, status, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas
from typing import List

 
Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def root():
    return "todo"


@app.post('/todo', response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate):
    
    session = Session(bind=engine, expire_on_commit=False)
    todo = models.ToDo(task = todo.task)
    session.add(todo)
    session.commit()
    id = todo.id
    session.refresh(todo)
    session.close()
    
    return todo


@app.get('/todo/{id}', response_model=schemas.ToDo)
def get_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    session.close()
    if not todo:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return todo

@app.put('/todo/{id}')
def update_todo(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    if todo:
        todo.task = task
        session.commit()
    session.close()
    if not todo:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return todo


@app.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    if todo:
        session.delete(todo)
        session.commit()
    session.close()
    if not todo:
        raise HTTPException(status=404, detail=f"todo item with id {id} does not Exist")
    return None


@app.get('/todo', response_model = List[schemas.ToDo])
def read_todo_list():
    session = Session(bind=engine, expire_on_commit=False)
    todo_list = session.query(models.ToDo).all()
    session.close()
    return todo_list