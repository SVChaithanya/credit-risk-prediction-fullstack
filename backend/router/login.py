from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db

from models import Registration
from schemas import Verify
from auth import verify_password, create_access_token, create_refresh_token,OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(Registration).filter(Registration.customer_id==data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(data.password,user.password):
        raise HTTPException(status_code=404,detail="password is invalid...")
    if not user.verfication_states:
        raise HTTPException(status_code=402,detail="verification is not done")

    
    access_token = create_access_token(user.customer_id)
    refresh_token = create_refresh_token(user.customer_id, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }