# backend/app/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # App
    APP_ENV: str = "development"
    PORT: int = 8000
    SECRET_KEY: str = "change-me"

    # Hashing scheme
    HASH_SCHEME: str = "argon2"

    # Argon2 params (значения по-умолчанию можно переопределить в .env)
    ARGON2_TIME_COST: int = 3
    ARGON2_MEMORY_COST: int = 65536
    ARGON2_PARALLELISM: int = 4
    ARGON2_HASH_LEN: int = 32
    ARGON2_SALT_LEN: int = 16

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
