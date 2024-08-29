from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import BaseIdModel


class Note(BaseIdModel):
    """
    Модель таблицы заметки.

    :param text: Текст заметки.
    :param created_at: Дата и время создания заметки.
    :param updated_at: Дата и время последнего редактирования заметки.
    :param author_id: ID автора заметки.
    """

    __tablename__ = "notes"

    text: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="notes")  # type: ignore  # noqa: F821
