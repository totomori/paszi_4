# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Создаём engine на основе DATABASE_URL из settings
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# Declarative base используется и моделями, и Alembic
Base = declarative_base()

def get_db():
    """
    Зависимость FastAPI для получения сессии БД.
    Используется yield, чтобы корректно закрывать сессию.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
