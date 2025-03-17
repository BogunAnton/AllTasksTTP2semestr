# test_main.py
import pytest
from fastapi.testclient import TestClient
from task19 import app, User

client = TestClient(app)

# Тест регистрации пользователя
def test_register_user():
    response = client.post(
        "/register/",
        json={
            "username": "testuser",
            "age": 25,
            "email": "testuser@example.com",
            "password": "securepass"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully."

# Тест извлечения данных пользователя
def test_get_user():
    # Сначала зарегистрируем пользователя
    client.post(
        "/register/",
        json={
            "username": "testuser",
            "age": 25,
            "email": "testuser@example.com",
            "password": "securepass"
        }
    )
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()["message"] == "User found."

# Тест удаления данных пользователя
def test_delete_user():
    # Сначала зарегистрируем пользователя
    client.post(
        "/register/",
        json={
            "username": "testuser",
            "age": 25,
            "email": "testuser@example.com",
            "password": "securepass"
        }
    )
    response = client.delete("/users/testuser")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully."

def test_register_user_invalid_age():
    response = client.post(
        "/register/",
        json={
            "username": "testuser",
            "age": 120,
            "email": "testuser@example.com",
            "password": "securepass"
        }
    )
    assert response.status_code == 422  # Ожидаем код состояния 422 для ошибки валидации
    assert "detail" in response.json()


# Тест ошибки "пользователь не найден"
def test_get_user_not_found():
    response = client.get("/users/nonexistentuser")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
