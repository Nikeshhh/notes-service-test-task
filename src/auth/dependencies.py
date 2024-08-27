from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from src.database.connection import get_db
from src.auth.models import User
from src.auth.services import UserService, get_payload
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db)]):
    """
    Зависимость для создания UserService.
    """
    return UserService(session=session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """
    Получает из базы текущего пользователя и возвращает его в виде модели.
    """
    username = get_payload(token).get("username")
    user = await user_service.get_by_username(username)
    return user
