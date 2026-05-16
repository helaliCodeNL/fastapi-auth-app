from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

class TokenUtils:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            return None

class ResetTokenUtils:
    @staticmethod
    def create_reset_token(email: str) -> tuple:
        token = jwt.encode(
            {"email": email, "type": "password_reset"},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        expires = datetime.now(timezone.utc) + timedelta(hours=24)
        return token, expires

    @staticmethod
    def verify_reset_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "password_reset":
                return None
            return payload.get("email")
        except JWTError:
            return None
