from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.database import SessionLocal
from app.logging_conf import logger

router = APIRouter(prefix="/api", tags=["register"])


# Dependency — получить сессию БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(payload, db)

    logger.info(f"Пользователь зарегистрирован: login={user.login}")

    return {"message": "user создан"}
