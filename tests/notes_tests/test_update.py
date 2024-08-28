from httpx import AsyncClient
import pytest

from src.notes.models import Note


UPDATE_URL = "notes/{note_id}"


@pytest.mark.anyio
async def test_update_note_success(
    async_client: AsyncClient, test_user_token: str, test_user_notes: list[Note]
):
    """
    Тестирует успешное обновление заметки. При этом текст исправляется валидатором.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "новаz замтка ползователяяя один"}
    note_id = test_user_notes[0].id
    async with async_client as ac:
        response = await ac.put(
            UPDATE_URL.format(note_id=note_id), headers=headers, json=data
        )
    assert response.status_code == 200
    r_data = response.json()
    assert r_data.get("text") == "новая заметка пользователя один"


@pytest.mark.anyio
async def test_update_note_success_no_fix(
    async_client: AsyncClient, test_user_token: str, test_user_notes: list[Note]
):
    """
    Тестирует успешное обновление заметки. При этом текст не изменяется.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "еще одна очередная заметка"}
    note_id = test_user_notes[0].id
    async with async_client as ac:
        response = await ac.put(
            UPDATE_URL.format(note_id=note_id), headers=headers, json=data
        )
    assert response.status_code == 200
    r_data = response.json()
    assert r_data.get("text") == "еще одна очередная заметка"


@pytest.mark.anyio
async def test_update_note_fail_not_found(
    async_client: AsyncClient, test_user_token: str, test_user_notes: list[Note]
):
    """
    Тестирует ошибку при попытке обновления несуществующей заметки.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "еще одна очередная заметка"}
    note_id = 727
    async with async_client as ac:
        response = await ac.put(
            UPDATE_URL.format(note_id=note_id), headers=headers, json=data
        )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_note_fail_wrong_author(
    async_client: AsyncClient, test_user_token: str, another_test_user_notes: list[Note]
):
    """
    Тестирует ошибку при попытке обновления заметки созданной другим пользователем.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    data = {"text": "еще одна очередная заметка"}
    note_id = another_test_user_notes[0].id
    async with async_client as ac:
        response = await ac.put(
            UPDATE_URL.format(note_id=note_id), headers=headers, json=data
        )
    assert response.status_code == 403
