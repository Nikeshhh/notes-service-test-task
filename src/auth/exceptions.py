from src.common.exceptions import BaseApplicationException


class AuthException(BaseApplicationException): ...


class LoginException(AuthException):
    status_code = 400
    detail = "Неправильное имя пользователя или пароль"


class TokenException(AuthException):
    status_code = 401
    detail = "Ошибка при валидации токена"
