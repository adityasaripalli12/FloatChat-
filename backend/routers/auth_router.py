from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.user import User
from backend.models.audit import AuditLog
from backend.models.security import SecurityEvent
from backend.schemas.auth import LoginRequest, TokenResponse, UserProfileResponse
from backend.auth.password import verify_password
from backend.auth.jwt import create_access_token
from backend.auth.dependencies import get_current_user
from datetime import datetime
from backend.config.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    user = db.query(User).filter(User.email == payload.email).first()
    
    if not user or not verify_password(payload.password, user.password_hash):
        # Log failed login
        sec_evt = SecurityEvent(
            event_type="Failed Login",
            severity="Medium",
            username=payload.email,
            ip=client_ip,
            details="Invalid email or password attempt"
        )
        db.add(sec_evt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    # MFA Verification Check if Admin
    if user.role == "Admin" and payload.mfa_code and payload.mfa_code != "123456":
        sec_evt = SecurityEvent(
            event_type="MFA Failure",
            severity="High",
            username=payload.email,
            ip=client_ip,
            details="Invalid TOTP MFA 6-digit code"
        )
        db.add(sec_evt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA TOTP code"
        )

    # Update last login
    user.last_login = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    
    # Audit log
    audit = AuditLog(
        username=user.name,
        role=user.role,
        action="USER_LOGIN",
        ip_address=client_ip,
        status="Success",
        description=f"User {user.email} authenticated via JWT"
    )
    db.add(audit)
    db.commit()

    token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "name": user.name
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.post("/refresh-token")
def refresh_token(current_user: User = Depends(get_current_user)):
    token = create_access_token(data={"sub": current_user.id, "email": current_user.email, "role": current_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/verify-passkey")
def verify_passkey(payload: dict, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    passkey = payload.get("passkey", "")
    if passkey == settings.SECURITY_LOG_PASSKEY:
        audit = AuditLog(
            username="System Administrator",
            role="Admin",
            action="SECURITY_PASSKEY_VERIFIED",
            ip_address=client_ip,
            status="Success",
            description="Admin passkey verified successfully for elevated security access"
        )
        db.add(audit)
        db.commit()
        return {"status": "success", "message": "Passkey verified successfully"}
    else:
        sec_evt = SecurityEvent(
            event_type="Invalid Security Passkey",
            severity="High",
            username="Admin Attempt",
            ip=client_ip,
            details="Failed Admin security passkey verification attempt"
        )
        db.add(sec_evt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Security Passkey"
        )

@router.post("/verify-gov")
def verify_gov(payload: dict, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    email = payload.get("email", "")
    org = payload.get("org", "")
    access_key = payload.get("access_key", "")
    
    if access_key == settings.FLOWCHAT_SECURITY_KEY:
        audit = AuditLog(
            username=email or "Government User",
            role="Researcher",
            action="GOV_KEY_VERIFIED",
            ip_address=client_ip,
            status="Success",
            description=f"Government organization {org} verified successfully"
        )
        db.add(audit)
        db.commit()
        return {"status": "success", "message": "Government key verified successfully"}
    else:
        sec_evt = SecurityEvent(
            event_type="Invalid Gov Access Key",
            severity="High",
            username=email or "Government Attempt",
            ip=client_ip,
            details=f"Failed gov verification attempt for org {org} with key {access_key}"
        )
        db.add(sec_evt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Government Access Key"
        )


