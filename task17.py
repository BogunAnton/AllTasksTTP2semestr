import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, constr, conint, Field, field_validator
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Определяем модель данных для пользователя с использованием Pydantic
class User(BaseModel):
    username: constr(min_length=1, strip_whitespace=True)  # Имя пользователя: минимальная длина 1, удаляем пробелы
    age: conint(gt=18)  # Возраст: должен быть больше 18
    email: EmailStr  # Email: должен быть валидным email-адресом
    password: constr(min_length=8, max_length=16)  # Пароль: длина от 8 до 16 символов
    phone: Optional[str] = None  # Телефон: необязательное поле

    # Пользовательский валидатор для поля age
    @field_validator('age')
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value > 110:
            raise ValueError('User age must be lower than 110')
        return value

# Обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Логируем информацию о запросе и ошибках валидации
    logger.error(f"Request URL: {request.url}, Method: {request.method}, Validation Error: {exc.errors()}")
    errors = []  # Список для хранения ошибок валидации
    for err in exc.errors():  # Перебираем все ошибки валидации
        loc = " -> ".join([str(loc) for loc in err['loc']])  # Формируем строку с местоположением ошибки
        input_value = err.get('input')  # Получаем значение ввода, вызвавшего ошибку
        # Обработка различных типов ошибок валидации
        if err['type'] == 'value_error.number.not_gt':  # Ошибка: значение не больше чем
            errors.append({
                "location": loc,
                "message": "Input should be greater than 18",  # Сообщение об ошибке
                "type": "value_error",  # Тип ошибки
                "input": input_value  # Вводимое значение
            })
        elif err['type'] == 'value_error.email':  # Ошибка: некорректный email
            errors.append({
                "location": loc,
                "message": 'Value is not a valid email address: An email address must have an @-sign.',
                "type": "value_error",
                "input": input_value
            })
        elif err['type'] == 'value_error.missing':  # Ошибка: обязательное поле отсутствует
            errors.append({
                "location": loc,
                "message": "Field is required",  # Сообщение об ошибке
                "type": "value_error",
                "input": input_value
            })
        elif err['type'] == 'value_error.any_str.min_length':  # Ошибка: строка слишком короткая
            errors.append({
                "location": loc,
                "message": "String should have at least 1 character",  # Сообщение об ошибке
                "type": "value_error",
                "input": input_value
            })
        elif err['type'] == 'value_error.any_str.max_length':  # Ошибка: строка слишком длинная
            errors.append({
                "location": loc,
                "message": "String should have at most 16 characters",  # Сообщение об ошибке
                "type": "value_error",
                "input": input_value
            })
        elif err['type'] == 'value_error':  # Обработка пользовательского валидатора
            errors.append({
                "location": loc,
                "message": err.get('msg', 'Unknown error occurred.'),  # Сообщение об ошибке
                "type": "value_error",
                "input": input_value
            })
        else:  # Обработка остальных ошибок
            errors.append({
                "location": loc,
                "message": err.get('msg', 'Unknown error occurred.'),  # Сообщение об ошибке
                "type": "unknown_error",
                "input": input_value
            })
    # Возвращаем ответ с ошибками валидации в формате JSON
    return JSONResponse(
        status_code=422,  # Код состояния 422 - ошибка валидации
        content={
            "message": "Validation error.",  # Сообщение об ошибке
            "errors": errors  # Список ошибок
        },
    )

# Эндпоинт для создания пользователя
@app.post("/users/")
async def create_user(user: User):
    logger.info(f"Creating user: {user}")  # Логируем создание пользователя
    # Возвращаем ответ с подтверждением создания пользователя, исключая пароль из ответа
    return JSONResponse(status_code=201,
                        content={"message": "User successfully created.", "user": user.model_dump(exclude={"password"})})

# Запуск приложения при выполнении этого скрипта
if __name__ == "__main__":
    import uvicorn  # Импортируем Uvicorn для запуска приложения
    logger.info("Starting the FastAPI application...")  # Логируем запуск приложения
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Запускаем приложение на локальном хосте
