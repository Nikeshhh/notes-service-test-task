from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
import jwt
import logging

from src.auth.exceptions import TokenException
from src.auth.models import User
from src.config import settings


logger = logging.getLogger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли пароль с зашифрованным паролем.

    :param plain_password: Проверяемый пароль.
    :param hashed_password: Зашифрованный пароль.
    :return: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Создает шифрованный пароль.

    :param password: Пароль для шифрования.
    :return: Шифрованный пароль.
    """
    return pwd_context.hash(password)


def create_token(username: str) -> str:
    """
    Создать новый токен для пользователя.

    :param username: str, имя пользователя.
    :return: str, токен для авторизации.
    """
    expire_time = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.TOKEN_EXPIRE_TIME
    )
    payload = {"username": username, "exp": expire_time}
    encoded_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_token


def get_payload(token: str) -> dict[str, str]:
    """
    Расшифровывает токен и возвращает его payload.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except jwt.InvalidTokenError as e:
        logger.error(e)
        raise TokenException
    return payload


class UserService:
    """
    Сервис для работы с пользователями.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        :param session: Сессия базы данных.
        """
        self._session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Получает пользователя из базы данных по username.

        :param username: Имя пользователя.
        :returns: Объект User найденного пользователя.
        """
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, username: str, password: str) -> User:
        """
        Создает нового пользователя.

        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        :returns: Объект User созданного пользователя.
        """
        hashed_password = hash_password(password)
        new_user = User(username=username, hashed_password=hashed_password)
        self._session.add(new_user)
        await self._session.commit()
        return new_user
