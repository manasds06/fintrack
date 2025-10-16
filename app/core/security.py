from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from ..core.database import get_db
from ..table_models.user_model import UserTable

# Load environment variables
load_dotenv()
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("ALGORITHM:", os.getenv("ALGORITHM"))

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2 scheme — this tells FastAPI how to find the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify & decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Verify token and return the current user object"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(UserTable).filter(UserTable.username == username).first()
    if user is None:
        raise credentials_exception

    return user