from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from httpx import AsyncClient

from src.common.exceptions import AccessViolationException, ResourceNotFound
from src.notes.models import Note
from src.config import settings


class YaSpellerService:
    """
    Сервис для работы с внешним сервисом Яндекс.Спеллер.
    """

    CHECK_TEXT_URL = "/checkText"

    def __init__(self, client: AsyncClient) -> None:
        self._options = settings.ya_speller_settings
        self._client = client

    async def validate_text(self, text: str) -> str:
        """
        Валидирует переданный текст.

        :returns: Валидированный текст.
        """
        data = {"text": text, "options": self._options}
        async with self._client as ac:
            response = await ac.get(self.CHECK_TEXT_URL, params=data)
        validation_errors = response.json()
        if validation_errors:
            text = self._fix_errors(text, validation_errors)
        return text

    def _fix_errors(self, text: str, errors: dict) -> str:
        """
        Исправляет ошибки, найденные в тексте спеллером.

        :param text: Изначальный текст.
        :param errors: Ответ спеллера, содержащий информацию об ошибках.
        """
        # Смещение относительно изначальной строки
        # Происходит из-за последовательной замены слов
        text_offset = 0
        for error in errors:
            # Заменяемое слово
            word = error.get("word")
            # Слово на которое производится замена
            replacement = error.get("s")[0]

            # Индекс начала слова
            start_pos = error.get("pos") + text_offset
            # Индекс конца слова
            end_pos = start_pos + error.get("len")

            # Заменить ошибочное слово
            text = self._perform_fix(text, start_pos, end_pos, replacement)
            # Расчет смещения
            text_offset += len(replacement) - len(word)
        return text

    def _perform_fix(
        self, text: str, start_pos: int, end_pos: int, replacement: str
    ) -> str:
        """
        Производит замену слова в строке.

        :param text: Строка, в которой происходит замена.
        :param start_pos: Индекс старта слова для замены.
        :param end_pos: Индекс конца слова для замены.
        :param replacement: Строка, на которую происходит замена.
        """
        return text[:start_pos] + replacement + text[end_pos:]


class NoteService:
    """
    Сервис для работы с заметками.
    """

    def __init__(
        self, session: AsyncSession, validation_service: YaSpellerService
    ) -> None:
        """
        :param session: Сессия базы данных.
        """
        self._session = session
        self._validation_service = validation_service

    async def create(self, text: str, user_id: int) -> Note:
        """
        Создает новую заметку.

        :param text: Текст заметки.
        :param user_id: ID пользователя, который создает заметку.
        :returns: Созданная заметка.
        """
        text = await self._validation_service.validate_text(text)
        new_note = Note(text=text, author_id=user_id)
        self._session.add(new_note)
        await self._session.commit()
        return new_note

    async def update(self, note_id: int, text: str, user_id: int) -> Note:
        """
        Обновляет текст существующей заметки.

        :param note_id: ID обновляемой заметки.
        :param text: Новый текст заметки.
        :param user_id: ID пользователя, который обновляет заметку.
        :raises ResourceNotFound: Если заметка не найдена.
        :raises AccessViolationException: Если заметка не принадлежит пользователю.
        :returns: Обновленная заметка.
        """
        text = await self._validation_service.validate_text(text)
        note = await self.get_by_id(note_id, user_id)
        note.text = text
        await self._session.commit()
        await self._session.refresh(note)
        return note

    async def get_by_id(self, id: int, user_id: int) -> Note:
        """
        Получить заметку по ID.

        :param id: ID заметки.
        :param user_id: ID пользователя, который получает заметку.
        :raises ResourceNotFound: Если заметка не найдена.
        :raises AccessViolationException: Если заметка не принадлежит пользователю.
        :returns: Найденную заметку.
        """
        stmt = select(Note).where(Note.id == id)
        result = await self._session.execute(stmt)
        note = result.scalar_one_or_none()
        if note is None:
            raise ResourceNotFound
        if note.author_id != user_id:
            raise AccessViolationException
        return note

    async def list_all(self, user_id: int) -> list[Note]:
        """
        Получить все заметки пользователя.

        :param user_id: ID пользователя, который получает заметки.
        :returns: Список заметок.
        """
        stmt = select(Note).where(Note.author_id == user_id)
        result = await self._session.execute(stmt)
        notes = result.scalars()
        return notes

    async def delete_by_id(self, id: int, user_id: int) -> None:
        """
        Удаляет заметку с переданным ID.

        :param id: ID заметки для удаления.
        :param user_id: ID пользователя, который удаляет заметку.
        :raises AccessViolationException: Если удаляемая заметка не принадлежит пользователю.
        """
        stmt = delete(Note).where(Note.id == id).where(Note.author_id == user_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise AccessViolationException
        await self._session.commit()
