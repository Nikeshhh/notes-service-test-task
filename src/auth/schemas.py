from pydantic import BaseModel, field_validator, model_validator


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegistrationSchema(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_is_equal(self):
        """
        Проверяет совпадают ли переданные пароли.
        """
        pw1 = self.password
        pw2 = self.password_repeat
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Пароли не совпадают")
        return self

    @field_validator("password")
    @classmethod
    def check_password_length(cls, password: str) -> str:
        """
        Проверяет, что длина пароля минимум 8 символов.
        """
        if len(password) < 8:
            raise ValueError("Минимальная длина пароля - 8 символов")
        return password
