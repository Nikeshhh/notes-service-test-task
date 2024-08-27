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


settings = Settings()
