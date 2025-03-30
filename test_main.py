from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base, DATABASE_URL
from models import Product

# Настройка тестовой базы данных
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Удаление таблицы products, если она существует
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS products CASCADE"))

# Создание таблиц в тестовой базе данных
Base.metadata.create_all(bind=engine)

# Переопределение зависимости для тестирования
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/products/",
        json={"title": "Test Product", "price": 19.99, "count": 100}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["price"] == 19.99
    assert data["count"] == 100

def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_product():
    # Создаем продукт для тестирования
    client.post("/products/", json={"title": "Test Product", "price": 19.99, "count": 100})
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Product"

def test_update_product():
    # Создаем продукт для тестирования
    client.post("/products/", json={"title": "Test Product", "price": 19.99, "count": 100})
    response = client.put(
        "/products/1",
        json={"title": "Updated Product", "price": 24.99, "count": 150}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Product"
    assert data["price"] == 24.99
    assert data["count"] == 150

