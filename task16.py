from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Пользовательские исключения с более подробными сообщениями
class CustomExceptionA(Exception):
    def __init__(self, detail: str = "CustomExceptionA occurred: The condition was not met."):
        self.detail = detail

class CustomExceptionB(Exception):
    def __init__(self, detail: str = "CustomExceptionB occurred: The item with the specified ID was not found."):
        self.detail = detail

# Обработчики исключений с более подробными ответами
@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "message": exc.detail,
            "details": "This error occurs when a specific condition is not met. Please check the input parameters and try again."
        },
    )

@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": exc.detail,
            "details": "This error occurs when the requested item ID does not exist. Please verify the ID and try again."
        },
    )

# Модель для ответов на ошибки
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: str

# Конечные точки API
@app.get("/trigger-a")
async def trigger_exception_a(condition: bool):
    if not condition:
        raise CustomExceptionA(detail="The condition provided was false, triggering CustomExceptionA.")
    return {"message": "CustomExceptionA not triggered"}

@app.get("/trigger-b/{item_id}")
async def trigger_exception_b(item_id: int):
    if item_id not in [1, 2, 3]:  # Предположим, что допустимые ID - 1, 2, 3
        raise CustomExceptionB(detail=f"Item with ID {item_id} not found, triggering CustomExceptionB.")
    return {"message": "CustomExceptionB not triggered", "item_id": item_id}
# :)