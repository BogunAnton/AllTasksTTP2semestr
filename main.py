from fastapi import FastAPI
from pydantic import BaseModel
from models import User

app = FastAPI()

class Numbers(BaseModel):
    num1: int
    num2: int

user = User(name="Bogun Anton", id=18)

@app.post("/calculate")
def calculate(numbers: Numbers):
    result = numbers.num1 + numbers.num2
    return {"result": result}

@app.get("/users")
def get_user():
    return user
