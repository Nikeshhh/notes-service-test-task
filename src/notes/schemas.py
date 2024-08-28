from datetime import datetime
from pydantic import BaseModel


class NoteOutSchema(BaseModel):
    """Схема для вывода заметки."""

    id: int
    author_id: int

    text: str

    created_at: datetime
    updated_at: datetime


class NoteInSchema(BaseModel):
    """Схема для ввода заметки"""

    text: str
