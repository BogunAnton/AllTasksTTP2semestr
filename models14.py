from sqlalchemy import Boolean, Column, Integer, String
from database14 import Base

class Todo(Base):
    __tablename__ = "ТТПtask14"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
