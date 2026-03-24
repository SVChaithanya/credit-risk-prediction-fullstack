from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from db import get_db
from models import Registration
from schemas import Register
from auth import generate_customer_id,hash_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):

    existing = db.query(Registration).filter(Registration.email == data.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    customer_id = generate_customer_id()
    verification = str(uuid.uuid4())

    user = Registration(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        customer_id=customer_id,
        verify=verification,
        password = hash_password(data.password)  
    )

    try:
        db.add(user)
        db.commit()
        return {"status": f"Customer {data.email} registered successfully" , "verification token": verification}
    except Exception as e:
        return {"error":str(e)}