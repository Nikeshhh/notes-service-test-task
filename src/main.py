from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from src.config import settings
from src.notes.handlers import router as notes_router
from src.logging import setup_logging

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    setup_logging()
    logger.debug(settings.postgres_url.unicode_string())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(notes_router)
