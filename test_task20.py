# test_task20.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from task20 import app, fetch_user_data_from_external_api

client = TestClient(app)

# Тест получения данных пользователя
@pytest.mark.asyncio
@patch("task20.fetch_user_data_from_external_api", new_callable=AsyncMock)
async def test_get_user(mock_fetch):
    mock_fetch.return_value = {"user_id": 1, "name": "Test User"}

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"user_data": {"user_id": 1, "name": "Test User"}}
    mock_fetch.assert_awaited_with(1)

# Тест сохранения данных
def test_save_data():
    response = client.post("/data/", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Data saved successfully.", "key": "test_key"}



