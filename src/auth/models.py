from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import BaseIdModel


class User(BaseIdModel):
    """
    Модель таблицы пользователя.

    :param username: Имя пользователя.
    :param hashed_password: Хешированный пароль пользователя.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    notes: Mapped[list["Note"]] = relationship(back_populates="author")  # type: ignore
