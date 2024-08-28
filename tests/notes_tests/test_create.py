from httpx import AsyncClient
import pytest

from src.auth.models import User


CREATE_URL = "notes/"


@pytest.mark.anyio
async def test_create_note_success(
    async_client: AsyncClient, test_user: User, test_user_token: str
):
    """
    Тестирует создание заметки без изменения изначального текста.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "Моя новая заметка без ошибок"}
    async with async_client as ac:
        response = await ac.post(CREATE_URL, json=data, headers=headers)
    assert response.status_code == 200
    r_data = response.json()
    assert r_data.get("text") == "Моя новая заметка без ошибок"
    assert r_data.get("author_id") == test_user.id


@pytest.mark.anyio
async def test_create_note_fixed(
    async_client: AsyncClient, test_user: User, test_user_token: str
):
    """
    Тестирует создание заметки. При этом текст исправляется сервисом валидации.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "Моя оваяяя заеткаа с плхй ошипкой"}
    async with async_client as ac:
        response = await ac.post(CREATE_URL, json=data, headers=headers)
    assert response.status_code == 200
    r_data = response.json()
    assert r_data.get("text") == "Моя новая заметка с плохой ошибкой"
    assert r_data.get("author_id") == test_user.id
