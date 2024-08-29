from typing import Any, Dict

from fastapi import HTTPException


class BaseApplicationException(HTTPException):
    def __init__(
        self,
        status_code: int = None,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        """
        Может это и не лучшая практика, но я считаю, что иметь шаблонные исключения - это удобно.
        """
        if status_code is None:
            status_code = self.status_code
        if detail is None:
            detail = self.detail
        super().__init__(status_code, detail, headers)


class AccessViolationException(BaseApplicationException):
    status_code = 403
    detail = "Вы не имеете доступа к этому действию"


class ResourceNotFound(BaseApplicationException):
    status_code = 404
    detail = "Запрашиваемый ресурс не найден"
