# 4 задание
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# 5 задание
# from pydantic import BaseModel
#
# class Feedback(BaseModel):
#     name: str
#     message: str
