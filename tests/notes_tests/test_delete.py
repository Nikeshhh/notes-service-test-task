from httpx import AsyncClient
import pytest

from src.notes.models import Note


DELETE_URL = "notes/{note_id}"


@pytest.mark.anyio
async def test_delete_note_success(
    async_client: AsyncClient, test_user_token: str, test_user_notes: list[Note]
):
    """
    Тестирует успешное удаление заметки.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    note_id = test_user_notes[0].id
    async with async_client as ac:
        response = await ac.delete(DELETE_URL.format(note_id=note_id), headers=headers)
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_note_fail_wrong_author(
    async_client: AsyncClient, test_user_token: str, another_test_user_notes: list[Note]
):
    """
    Тестирует ошибку при попытке удаления чужой заявки.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    note_id = another_test_user_notes[0].id
    async with async_client as ac:
        response = await ac.delete(DELETE_URL.format(note_id=note_id), headers=headers)
    assert response.status_code == 403


@pytest.mark.anyio
async def test_delete_note_fail_not_found(
    async_client: AsyncClient, test_user_token: str, another_test_user_notes: list[Note]
):
    """
    Тестирует ошибку при попытке удаления несуществующей заявки.
    """
    headers = {"Authorization": f"bearer {test_user_token}"}
    note_id = 727
    async with async_client as ac:
        response = await ac.delete(DELETE_URL.format(note_id=note_id), headers=headers)
    assert response.status_code == 403
