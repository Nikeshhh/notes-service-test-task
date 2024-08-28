from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field


class Settings(BaseSettings):
    """
    Класс для глобальных настроек приложения.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Данные для подключения к БД
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5431

    # Ключ для подписей токенов
    SECRET_KEY: str = "insecure-key"
    # Время жизни токена в минутах
    TOKEN_EXPIRE_TIME: int = 30
    # Алгоритм шифрования
    ALGORITHM: str = "HS256"

    # Базовый url сервиса Яндекс.Спеллер
    YA_SPELLER_BASE_URL: str = "https://speller.yandex.net/services/spellservice.json"
    # Пропускать слова с цифрами, например, "авп17х4534".
    IGNORE_DIGITS: bool = False
    # Пропускать интернет-адреса, почтовые адреса и имена файлов.
    IGNORE_URLS: bool = False
    # Подсвечивать повторы слов, идущие подряд. Например, "я полетел на на Кипр".
    FIND_REPEAT_WORDS: bool = False
    # Игнорировать неверное употребление ПРОПИСНЫХ/строчных букв, например, в слове "москва".
    IGNORE_CAPITALIZATION: bool = False

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        """
        Создает URL для подключения к Postgres.
        """
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @property
    def ya_speller_settings(self) -> int:
        """
        Собирает настройки Яндекс.Спеллера.

        Docs: https://yandex.ru/dev/speller/doc/ru/reference/speller-options
        """
        settings_sum = 0
        if self.IGNORE_DIGITS:
            settings_sum += 2
        if self.IGNORE_URLS:
            settings_sum += 4
        if self.FIND_REPEAT_WORDS:
            settings_sum += 8
        if self.IGNORE_CAPITALIZATION:
            settings_sum += 512
        return settings_sum


settings = Settings()
