from httpx import AsyncClient
import pytest

from src.auth.models import User


LOGIN_URL = "auth/token"


@pytest.mark.anyio
async def test_login_success(async_client: AsyncClient, test_user: User):
    """
    Тестирует успешный вход.
    """
    data = {"username": "testuser", "password": "12345678"}
    async with async_client as ac:
        response = await ac.post(LOGIN_URL, data=data)
    assert response.status_code == 200, response.json()


@pytest.mark.anyio
async def test_login_wrong_password(async_client: AsyncClient, test_user: User):
    """
    Тестирует ошибку входа при неправильном пароле.
    """
    data = {"username": "testuser", "password": "1234567890"}
    async with async_client as ac:
        response = await ac.post(LOGIN_URL, data=data)
    assert response.status_code == 400, response.json()


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient, test_user: User):
    """
    Тестирует ошибку входа при несуществующем логине.
    """
    data = {"username": "wrongusername", "password": "1234567890"}
    async with async_client as ac:
        response = await ac.post(LOGIN_URL, data=data)
    assert response.status_code == 400, response.json()
