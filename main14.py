from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database14 import SessionLocal, engine, Base
from models14 import Todo
from contextlib import asynccontextmanager

# Создаем базу данных
"""async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)"""

app = FastAPI()

"""@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем базу данных при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Здесь можно добавить код для очистки при завершении"""

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# Схема для запросов
class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

# CRUD операции
@app.post("/todos/", response_model=TodoCreate)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.get("/todos/{todo_id}", response_model=TodoCreate)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoUpdate)
async def update_todo(todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(db_todo)
    await db.commit()
    return {"detail": "Todo deleted"}
