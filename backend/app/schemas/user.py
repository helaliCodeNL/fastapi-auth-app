from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TwoFASetup(BaseModel):
    secret: str
    qr_code: str

class TwoFAVerify(BaseModel):
    token: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    phone: Optional[str]
    is_active: bool
    is_verified: bool
    two_fa_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True
