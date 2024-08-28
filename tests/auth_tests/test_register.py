from httpx import AsyncClient
import pytest


REGISTER_URL = "auth/register"


@pytest.mark.anyio
async def test_register_success(async_client: AsyncClient):
    """
    Тестирует успешную регистрацию нового пользователя.
    """
    data = {
        "username": "testuser1",
        "password": "asdfasdf",
        "password_repeat": "asdfasdf",
    }
    async with async_client as ac:
        response = await ac.post(REGISTER_URL, json=data)
    assert response.status_code == 200, response.json()


@pytest.mark.anyio
async def test_register_fail_on_passwords_not_matching(async_client: AsyncClient):
    """
    Тестирует ошибку при регистрации, когда пароли не совпадают.
    """
    data = {
        "username": "testuser1",
        "password": "asdfasdf",
        "password_repeat": "qwerqwer",
    }
    async with async_client as ac:
        response = await ac.post(REGISTER_URL, json=data)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_fail_on_password_too_short(async_client: AsyncClient):
    """
    Тестирует ошибку при регистрации, когда пароль слишком короткий.
    """
    data = {"username": "testuser1", "password": "asdf", "password_repeat": "asdf"}
    async with async_client as ac:
        response = await ac.post(REGISTER_URL, json=data)
    assert response.status_code == 422
