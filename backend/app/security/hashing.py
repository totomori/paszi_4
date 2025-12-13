# backend/app/security/hashing.py
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from app.config import settings


# Создаём PasswordHasher на основе параметров из settings
pwd_hasher = PasswordHasher(
    time_cost=settings.ARGON2_TIME_COST,
    memory_cost=settings.ARGON2_MEMORY_COST,
    parallelism=settings.ARGON2_PARALLELISM,
    hash_len=settings.ARGON2_HASH_LEN,
    salt_len=settings.ARGON2_SALT_LEN,
)


def hash_password(plain_password: str) -> str:
    """
    Хэширует пароль и возвращает строку-хэш (включая соль).
    """
    return pwd_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль против хэша.
    Возвращает True при совпадении, False при несовпадении.
    """
    try:
        return pwd_hasher.verify(hashed_password, plain_password)
    except argon2_exceptions.VerifyMismatchError:
        return False
    except argon2_exceptions.VerificationError:
        # другие ошибки верификации считаем как False
        return False
