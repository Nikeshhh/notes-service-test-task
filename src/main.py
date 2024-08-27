from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from src.config import settings
from src.notes.handlers import router as notes_router
from src.auth.handlers import router as auth_router
from src.logging import setup_logging


logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    setup_logging()
    logger.debug(settings.postgres_url.unicode_string())
    if settings.SECRET_KEY == "insecure-key":
        logger.warning(
            "Секретный ключ приложения не задан. Используется небезопасный ключ по умолчанию"
        )
    yield


app = FastAPI(
    title="Notes service for KODE",
    description="Сервис для создания заметок с валидацией от Яндекс.Спеллер",
    lifespan=lifespan,
)
app.include_router(notes_router)
app.include_router(auth_router)
