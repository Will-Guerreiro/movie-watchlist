import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user : UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    new_user = User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(login : UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login.email).first()
    if not user:
        raise HTTPException(status_code=401,
                            detail="Incorrect email or password")

    assert isinstance(user, User)
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=401,
                            detail="Incorrect email or password")

    return create_access_token(user)

@router.post("/get-user-id", response_model=UserResponse)
def get_user_id(current_user = Depends(get_current_user)) -> UserResponse:
    return current_user