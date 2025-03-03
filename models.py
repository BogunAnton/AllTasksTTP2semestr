from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import re

app = FastAPI()

# Регулярное выражение для проверки формата Accept-Language
accept_language_pattern = re.compile(r'^[a-zA-Z]{2,3}(-[a-zA-Z]{2,3})?(;q=[0-9]\.[0-9])?(,[a-zA-Z]{2,3}(-[a-zA-Z]{2,3})?(;q=[0-9]\.[0-9])?)*$')

@app.get("/headers")
async def get_headers(request: Request):
    # Извлечение заголовков
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")

    # Проверка наличия заголовков
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing 'User-Agent' header")

    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing 'Accept-Language' header")

    # Проверка формата Accept-Language
    if not accept_language_pattern.match(accept_language):
        raise HTTPException(status_code=400, detail="Invalid format for 'Accept-Language' header")

    # Возвращение заголовков в формате JSON
    return JSONResponse(content={
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    })

# Запуск приложения с помощью Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
