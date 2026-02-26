from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.security import create_access_token
import random

router = APIRouter(prefix="/auth", tags=["auth"])

# Simplified OTP store (In production, use Redis)
otp_store = {}

@router.post("/request-otp")
def request_otp(email: str):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp
    print(f"OTP for {email}: {otp}") # Simulating email send
    return {"message": "OTP sent to email"}

@router.post("/verify-otp")
def verify_otp(email: str, otp: str):
    if otp_store.get(email) == otp:
        token = create_access_token(subject=email)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid OTP")
