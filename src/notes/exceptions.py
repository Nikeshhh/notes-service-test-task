from src.common.exceptions import BaseApplicationException


class NoteException(BaseApplicationException): ...


class YaSpellerValidationException(NoteException):
    status_code = 400
