
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional
import uuid

app = FastAPI()

# Примерные учетные данные (в реальном приложении используйте базу данных)
fake_users_db = {
    "user123": "password123"
}

# Примерные данные сессий (в реальном приложении используйте базу данных)
fake_sessions_db = {}

# Маршрут для входа в систему
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if fake_users_db.get(username) == password:
        session_token = str(uuid.uuid4())
        fake_sessions_db[session_token] = username
        response = JSONResponse(content={"message": "Logged in successfully"})
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True  # Включите это в продакшене, если используете HTTPS
        )
        return response
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Зависимость для проверки аутентификации
async def verify_token(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in fake_sessions_db:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return fake_sessions_db[session_token]

# Защищенный маршрут для получения информации о пользователе
@app.get("/user")
async def get_user(username: str = Depends(verify_token)):
    return JSONResponse(content={"message": f"Hello, {username}!"})

# Запуск приложения с помощью Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
