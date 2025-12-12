from pydantic import BaseModel, Field, validator
import re


# -----------------------
# Схема входящих данных
# -----------------------
class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8)

    @validator("login")
    def validate_login(cls, v):
        pattern = r"^[A-Za-z0-9._-]{3,32}$"
        if not re.match(pattern, v):
            raise ValueError(
                "login должен быть 3–32 символа, латиница, цифры, спецсимволы . _ -"
            )
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("пароль должен быть минимум 8 символов")

        if not re.search(r"[A-Z]", v):
            raise ValueError("пароль должен содержать минимум 1 заглавную букву")

        if not re.search(r"[a-z]", v):
            raise ValueError("пароль должен содержать минимум 1 строчную букву")

        if not re.search(r"\d", v):
            raise ValueError("пароль должен содержать минимум 1 цифру")

        if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]", v):
            raise ValueError("пароль должен содержать минимум 1 спецсимвол")

        return v


# -----------------------
# Схема ответа API
# -----------------------
class UserResponse(BaseModel):
    id: int
    login: str

    class Config:
        orm_mode = True
