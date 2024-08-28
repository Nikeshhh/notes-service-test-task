from typing import Annotated
from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.notes.dependencies import get_note_service
from src.notes.services import NoteService
from src.notes.schemas import NoteInSchema, NoteOutSchema


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/{note_id}")
async def get_note(
    note_id: int,
    note_service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NoteOutSchema:
    """
    Получить заметку по ID.
    """
    note = await note_service.get_by_id(id=note_id, user_id=current_user.id)
    return note


@router.get("/")
async def list_notes(
    note_service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[NoteOutSchema]:
    """
    Получить все заметки текущего пользователя.
    """
    notes = await note_service.list_all(current_user.id)
    return notes


@router.post("/")
async def create_note(
    note_data: NoteInSchema,
    note_service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NoteOutSchema:
    """
    Создать новую заметку.
    """
    note = await note_service.create(text=note_data.text, user_id=current_user.id)
    return note


@router.put("/{note_id}")
async def update_note(
    note_id: int,
    note_data: NoteInSchema,
    note_service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NoteOutSchema:
    """
    Изменить текст существующей заметки.
    """
    updated_note = await note_service.update(
        note_id=note_id, text=note_data.text, user_id=current_user.id
    )
    return updated_note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    note_service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Удалить заметку.
    """
    await note_service.delete_by_id(id=note_id, user_id=current_user.id)
