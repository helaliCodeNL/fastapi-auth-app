from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ...database import get_db
from ...models.user import User
from ...schemas.user import UserRegister, UserLogin, TwoFASetup, TwoFAVerify, PasswordReset, PasswordResetConfirm
from ...core.security import PasswordUtils, TokenUtils, ResetTokenUtils
from ...core.twofa import TwoFAUtils
from ...core.email import EmailUtils

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        name=user.name,
        phone=user.phone,
        hashed_password=PasswordUtils.hash_password(user.password),
        is_verified=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    EmailUtils.send_welcome_email(user.email, user.name)
    
    return {"message": "User registered", "user_id": new_user.id}

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not PasswordUtils.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.two_fa_enabled:
        return {"requires_2fa": True, "email": user.email}

    access_token = TokenUtils.create_access_token({"sub": user.id, "email": user.email})
    refresh_token = TokenUtils.create_refresh_token({"sub": user.id, "email": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "name": user.name
    }

@router.post("/setup-2fa")
def setup_2fa(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secret = TwoFAUtils.generate_secret()
    print(f"\n=== 2FA CODE ===")
    print(f"User: {user.email}")
    print(f"Code: {secret}")
    print("===============\n")
    
    user.two_fa_secret = secret
    db.commit()

    return {"secret": secret}

@router.post("/verify-2fa")
def verify_2fa(data: TwoFAVerify, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.two_fa_secret:
        raise HTTPException(status_code=404, detail="2FA not setup")

    if not TwoFAUtils.verify_token(user.two_fa_secret, data.token):
        raise HTTPException(status_code=400, detail="Invalid code")

    user.two_fa_enabled = True
    db.commit()

    return {"message": "2FA enabled"}

@router.post("/login-2fa")
def login_2fa(email: str, token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.two_fa_enabled:
        raise HTTPException(status_code=401, detail="Invalid")

    if not TwoFAUtils.verify_token(user.two_fa_secret, token):
        raise HTTPException(status_code=401, detail="Invalid code")

    access_token = TokenUtils.create_access_token({"sub": user.id, "email": user.email})
    refresh_token = TokenUtils.create_refresh_token({"sub": user.id, "email": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "name": user.name
    }

@router.post("/forgot-password")
def forgot_password(data: PasswordReset, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        code, expires = ResetTokenUtils.create_reset_token(user.email)
        user.password_reset_token = code
        user.password_reset_expires = expires
        db.commit()
        
        print(f"\n=== PASSWORD RESET CODE ===")
        print(f"Email: {user.email}")
        print(f"Code: {code}")
        print("===========================\n")
        
        EmailUtils.send_password_reset_email(user.email, code)
    
    return {"message": "If email exists, reset code sent"}

@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    # Find user by reset code
    user = db.query(User).filter(User.password_reset_token == data.token).first()
    if not user or not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    user.hashed_password = PasswordUtils.hash_password(data.password)
    user.password_reset_token = None
    user.password_reset_expires = None
    db.commit()

    return {"message": "Password reset successfully"}

@router.post("/refresh")
def refresh(refresh_token: str):
    payload = TokenUtils.verify_token(refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token = TokenUtils.create_access_token({"sub": payload["sub"], "email": payload.get("email")})
    return {"access_token": access_token, "token_type": "bearer"}
