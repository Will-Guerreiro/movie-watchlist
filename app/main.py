from app.database import engine, SessionLocal, Base
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.routers import users
from app.schemas import UserCreate

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "API is running"}
