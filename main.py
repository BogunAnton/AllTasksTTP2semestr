# 4 задание
from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post("/user")
async def check_adult(user: User):
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }

# 5 задание
# from fastapi import FastAPI
# from models import Feedback
#
# app = FastAPI()
#
# # Список для хранения отзывов
# feedback_list = []
#
# @app.post("/feedback")
# async def submit_feedback(feedback: Feedback):
#     # Сохраняем отзыв в списке
#     feedback_list.append(feedback)
#
#     # Возвращаем сообщение об успешном завершении
#     return {
#         "message": f"Feedback received. Thank you, {feedback.name}!"