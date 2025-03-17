# task20.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# Модель данных для хранения информации о пользователе
class UserData(BaseModel):
    user_id: int
    name: str

# Внешняя зависимость: функция для получения данных пользователя из внешнего API
async def fetch_user_data_from_external_api(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching user data")
        return response.json()

# Конечная точка для получения данных пользователя
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user_data = await fetch_user_data_from_external_api(user_id)
    return {"user_data": user_data}

# Модель данных для сохранения данных
class DataModel(BaseModel):
    key: str
    value: str

# Простая "база данных" для хранения данных
database = {}

# Конечная точка для сохранения данных
@app.post("/data/")
async def save_data(data: DataModel):
    database[data.key] = data.value
    return {"message": "Data saved successfully.", "key": data.key}
# :)