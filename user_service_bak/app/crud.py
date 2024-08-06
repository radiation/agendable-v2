from datetime import datetime
from uuid import uuid4

from models import User
from schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=str(uuid4()),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
        date_joined=user.date_joined or datetime.now(datetime.UTC),
    )
    # Add password hashing here
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    for var, value in vars(user_update).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
