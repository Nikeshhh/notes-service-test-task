from typing import Any, Dict
from fastapi import HTTPException


class AuthException(HTTPException):
    def __init__(self, status_code: int = None, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        if status_code is None:
            status_code = self.status_code
        if detail is None:
            detail = self.detail
        super().__init__(status_code, detail, headers)


class LoginException(AuthException):
    status_code = 400
    detail = "Неправильное имя пользователя или пароль"


class TokenException(AuthException):
    status_code = 401
    detail = "Ошибка при валидации токена"
