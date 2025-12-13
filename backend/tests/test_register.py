import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings

# -----------------------------
# ТЕСТОВАЯ БАЗА ДАННЫХ
# -----------------------------

# SQLite in-memory (быстро и безопасно)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Создаем структуру таблиц в тестовой БД
Base.metadata.create_all(bind=engine)


# -----------------------------
# ЗАМЕНЯЕМ get_db ДЛЯ ТЕСТОВ
# -----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# -----------------------------
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# -----------------------------

def register(login: str, password: str):
    return client.post(
        "/api/register",
        json={"login": login, "password": password},
    )


# -----------------------------
# ТЕСТ 1: УСПЕШНАЯ РЕГИСТРАЦИЯ
# -----------------------------
def test_success_registration():
    response = register(
        login="test_user",
        password="StrongPass1!"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "user создан"}


# -----------------------------
# ТЕСТ 2: КОНФЛИКТ ЛОГИНА
# -----------------------------
def test_conflict_login():
    # Первый запрос — успешный
    register("duplicate", "StrongPass1!")

    # Второй запрос — должен дать 409
    response = register("duplicate", "StrongPass1!")
    assert response.status_code == 409
    assert "уже существует" in response.json()["detail"]


# -----------------------------
# ТЕСТ 3: СЛАБЫЙ ПАРОЛЬ
# -----------------------------
def test_weak_password():
    response = register(
        login="weakuser",
        password="123"  # слабый
    )
    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]
