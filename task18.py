import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, constr, conint, Field
from typing import Optional
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка файлового обработчика для записи ошибок в файл
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)

# Создаем обработчик, который записывает ошибки в файл
file_handler = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
error_logger.addHandler(file_handler)

app = FastAPI()

class User(BaseModel):
    username: constr(min_length=1, strip_whitespace=True)
    age: conint(gt=18, lt=110)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = None

class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message

class InvalidUserDataException(Exception):
    def __init__(self, message="Invalid user data provided"):
        self.message = message

users_db = []  # Простая "база данных" для хранения пользователей

@app.post("/register/")
async def register_user(user: User):
    if user.age > 110:
        raise InvalidUserDataException("Age cannot be greater than 110")
    users_db.append(user)
    return {"message": "User registered successfully.", "user": user.model_dump(exclude={"password"})}

@app.get("/users/{username}")
async def get_user(username: str):
    for user in users_db:
        if user.username == username:
            return {"message": "User found.", "user": user.model_dump(exclude={"password"})}
    raise UserNotFoundException()

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    error_logger.error(f"User not found: {exc.message}")
    response = ErrorResponseModel(
        status_code=404,
        message=exc.message,
        error_code="USER_NOT_FOUND"
    )
    return JSONResponse(
        status_code=404,
        content=response.model_dump(),
        headers={"X-ErrorHandleTime": str(datetime.utcnow())}
    )

@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_exception_handler(request: Request, exc: InvalidUserDataException):
    error_logger.error(f"Invalid user data: {exc.message}")
    response = ErrorResponseModel(
        status_code=400,
        message=exc.message,
        error_code="INVALID_USER_DATA"
    )
    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
        headers={"X-ErrorHandleTime": str(datetime.utcnow())}
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the FastAPI application...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

