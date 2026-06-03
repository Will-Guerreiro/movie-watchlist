import passlib
from passlib.context import CryptContext
from jose import jwt
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: User):
    payload = {
        "sub" : str(user.id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
