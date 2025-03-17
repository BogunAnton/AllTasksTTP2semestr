# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr, conint
from typing import List

app = FastAPI()

# Модель данных для пользователя
class User(BaseModel):
    username: constr(min_length=1, strip_whitespace=True)
    age: conint(gt=18, lt=110)
    email: EmailStr
    password: constr(min_length=8, max_length=16)

# Простая "база данных" для хранения пользователей
users_db: List[User] = []

# Регистрация пользователя
@app.post("/register/")
async def register_user(user: User):
    if user.age > 110:
        raise HTTPException(status_code=400, detail="Age cannot be greater than 110")
    users_db.append(user)
    return {"message": "User registered successfully.", "user": user.model_dump(exclude={"password"})}

# Извлечение данных пользователя
@app.get("/users/{username}")
async def get_user(username: str):
    for user in users_db:
        if user.username == username:
            return {"message": "User found.", "user": user.model_dump(exclude={"password"})}
    raise HTTPException(status_code=404, detail="User not found")

# Удаление данных пользователя
@app.delete("/users/{username}")
async def delete_user(username: str):
    global users_db
    users_db = [user for user in users_db if user.username != username]
    return {"message": "User deleted successfully."}
