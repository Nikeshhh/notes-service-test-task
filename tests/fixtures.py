from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from src.auth.services import UserService, create_token
from src.auth.models import User


@pytest.fixture
async def test_user(async_db: AsyncSession) -> User:
    user = await UserService(async_db).create_user(
        username="testuser", password="12345678"
    )
    return user


@pytest.fixture
async def test_user_token(test_user: User) -> str:
    return create_token(test_user.username)
