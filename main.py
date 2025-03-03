from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(None, ge=0)
    is_subscribed: bool = False

@app.post("/create_user")
async def create_user(user: UserCreate):
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)