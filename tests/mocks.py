from src.notes.services import YaSpellerService


class MockYaSpellerService(YaSpellerService):
    """
    Сервис для подмены сервиса валидации при создании фикстур.
    """

    def __init__(self) -> None:
        pass

    async def validate_text(self, text: str) -> str:
        """
        Возвращает изначальный текст без изменений.
        """
        return text
