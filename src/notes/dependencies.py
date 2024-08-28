from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.notes.services import NoteService, YaSpellerService
from src.database.connection import get_db
from src.config import settings


async def get_ya_speller_client() -> AsyncClient:
    """
    Зависимость для создания http-клиента для работы с Яндекс.Спеллером.
    """
    return AsyncClient(base_url=settings.YA_SPELLER_BASE_URL)


async def get_ya_speller_service(
    async_http_client: Annotated[AsyncClient, Depends(get_ya_speller_client)],
) -> YaSpellerService:
    """
    Зависимость для создания сервиса валидации Яндекс.Спеллер.
    """
    return YaSpellerService(async_http_client)


async def get_note_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    validation_service: Annotated[YaSpellerService, Depends(get_ya_speller_service)],
) -> NoteService:
    """
    Зависимость для создания NoteService.
    """
    return NoteService(session=session, validation_service=validation_service)
