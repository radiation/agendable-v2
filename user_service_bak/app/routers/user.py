from app import db
from app.crud import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
)
from app.schemas import User, UserCreate, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(db.get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(db.get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(
    user_id: str, user: UserUpdate, db: Session = Depends(db.get_db)
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, db_user, user)


@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: str, db: Session = Depends(db.get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, user_id=user_id)
