from httpx import AsyncClient
import pytest


LIST_URL = "notes/"


@pytest.mark.anyio
async def test_list_notes_success(
    async_client: AsyncClient, test_user_token: str, create_test_notes
):
    """
    Тестирует успешное получение списка заметок для первого пользователя.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    async with async_client as ac:
        response = await ac.get(LIST_URL, headers=headers)
    assert response.status_code == 200
    r_data = response.json()
    assert len(r_data) == 3


@pytest.mark.anyio
async def test_list_notes_another_user_success(
    async_client: AsyncClient, another_test_user_token: str, create_test_notes
):
    """
    Тестирует успешное получение списка заметок для второго пользователя.
    """
    headers = {"Authorization": f"bearer {another_test_user_token}"}
    async with async_client as ac:
        response = await ac.get(LIST_URL, headers=headers)
    assert response.status_code == 200
    r_data = response.json()
    assert len(r_data) == 4
