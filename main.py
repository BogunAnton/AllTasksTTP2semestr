from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Импортируем только необходимые модули
import crud
import models
import schemas
from database import SessionLocal, engine

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание продукта
@app.post("/products/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

# Чтение списка продуктов
@app.get("/products/", response_model=list[schemas.ProductRead])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

# Чтение одного продукта
@app.get("/products/{product_id}", response_model=schemas.ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Обновление продукта
@app.put("/products/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Удаление продукта
@app.delete("/products/{product_id}", response_model=schemas.ProductRead)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
