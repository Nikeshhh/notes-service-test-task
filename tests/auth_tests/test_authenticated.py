from httpx import AsyncClient
import pytest


AUTHENTICATED_URL = "auth/test"


@pytest.mark.anyio
async def test_authenticated_success(async_client: AsyncClient, test_user_token: str):
    """
    Тестирует успешную авторизацию по токену.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    async with async_client as ac:
        response = await ac.get(AUTHENTICATED_URL, headers=headers)
    assert response.status_code == 200, response.json()
    assert response.json() == "testuser"


@pytest.mark.anyio
async def test_not_authenticated_token_error(
    async_client: AsyncClient, test_user_token: str
):
    """
    Тестирует ошибку авторизации при неправильном токене.
    """
    headers = {"Authorization": "bearer asdfasdf"}
    async with async_client as ac:
        response = await ac.get(AUTHENTICATED_URL, headers=headers)
    assert response.status_code == 400, response.json()
