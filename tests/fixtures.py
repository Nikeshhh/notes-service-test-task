from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from src.notes.services import NoteService, YaSpellerService
from src.notes.models import Note
from src.auth.services import UserService, create_token
from src.auth.models import User
from tests.mocks import MockYaSpellerService


@pytest.fixture
async def test_user(async_db: AsyncSession) -> User:
    user = await UserService(async_db).create_user(
        username="testuser", password="12345678"
    )
    return user


@pytest.fixture
async def another_test_user(async_db: AsyncSession) -> User:
    user = await UserService(async_db).create_user(
        username="anothertestuser", password="12345678"
    )
    return user


@pytest.fixture
async def test_user_token(test_user: User) -> str:
    return create_token(test_user.username)


@pytest.fixture
async def another_test_user_token(another_test_user: User) -> str:
    return create_token(another_test_user.username)


@pytest.fixture
async def test_user_notes(note_service: NoteService, test_user: User) -> list[Note]:
    notes = []
    for i in range(1, 4):
        notes.append(
            await note_service.create(text=f"Заметка номер {i}", user_id=test_user.id)
        )
    return notes


@pytest.fixture
async def another_test_user_notes(
    note_service: NoteService, another_test_user: User
) -> list[Note]:
    notes = []
    for i in range(4, 8):
        notes.append(
            await note_service.create(
                text=f"Заметка номер {i}", user_id=another_test_user.id
            )
        )
    return notes


@pytest.fixture
async def speller_service() -> YaSpellerService:
    return MockYaSpellerService()


@pytest.fixture
async def note_service(
    async_db: AsyncSession, speller_service: YaSpellerService
) -> NoteService:
    return NoteService(session=async_db, validation_service=speller_service)


@pytest.fixture
async def create_test_notes(
    test_user_notes: list[Note], another_test_user_notes: list[Note]
) -> None: ...
