from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.database import get_db


router = APIRouter()

@router.post("/users")
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name = user.name,
        email = user.email,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }