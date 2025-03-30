from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    title: str
    price: float
    count: int

class ProductRead(BaseModel):
    id: int
    title: str
    price: float
    count: int

    model_config = ConfigDict(from_attributes=True)

