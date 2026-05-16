from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import TokenUtils

router = APIRouter()

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]
    payload = TokenUtils.verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "phone": current_user.phone,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "two_fa_enabled": current_user.two_fa_enabled,
        "created_at": current_user.created_at
    }

@router.post("/disable-2fa")
def disable_2fa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.two_fa_enabled = False
    current_user.two_fa_secret = None
    db.commit()
    return {"message": "2FA disabled"}
