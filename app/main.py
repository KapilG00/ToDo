from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from .db import get_db, engine, Base
from .models import Todo
from .schemas import TodoCreate, TodoRead, TodoUpdate
from typing import List
from sqlalchemy.exc import SQLAlchemyError


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo FastAPI App", version="1.0")


@app.get("/")
async def root(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        print("Successfully connected to the database!")
    except Exception as e:
        print("Database connection error:", e)
        raise e
    return {"message": "Welcome to ToDo app!!"}

# Get all todos.
@app.get("/todo", response_model=List[TodoRead])
async def get_all_todos(db: Session = Depends(get_db)) -> List[TodoRead]:
    todo_data = db.query(Todo).all()
    return todo_data

# Get a todo.
@app.get("/todo/{todo_id}", response_model=TodoRead)
async def get_todo(todo_id: int, db: Session = Depends(get_db)) -> TodoRead:
    todo_data = db.query(Todo).filter(Todo.id==todo_id).first()
    return todo_data

# Create a todo.
@app.post("/todo", response_model=TodoRead)
async def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)) -> TodoRead:
    try:
        todo_obj = Todo(**todo_data.dict())
        db.add(todo_obj)
        db.commit()
        db.refresh(todo_obj)
        return todo_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
# Update a todo.
@app.put("/todo/{todo_id}", response_model=TodoRead)
async def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)) -> TodoRead:
    try:
        todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo_obj:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        for key, value in todo_data.model_dump(exclude_unset=True).items():
            setattr(todo_obj, key, value)

        db.commit()
        db.refresh(todo_obj)
        return todo_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )





