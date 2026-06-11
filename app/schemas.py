from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    name : str
    email : str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class ListCreate(BaseModel):
    name: str

class ListResponse(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime

class AddListMember(BaseModel):
    email: str