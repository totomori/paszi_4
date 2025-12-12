from sqlalchemy.orm import Session
from app.models.user import User
from app.security.hashing import hash_password
from app.schemas.user import UserCreate
from fastapi import HTTPException


def create_user(data: UserCreate, db: Session):
    # Проверка уникальности логина
    existing = db.query(User).filter(User.login == data.login).first()
    if existing:
        raise HTTPException(status_code=409, detail="логин уже существует")

    # Хэширование пароля
    hashed = hash_password(data.password)

    user = User(
        login=data.login,
        password_hash=hashed,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
