from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Registration
from schemas import Verify


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/verify")
def verify(data:Verify, db: Session = Depends(get_db)):

    existing = db.query(Registration).filter(Registration.verify == data.token).first()

    if not existing:
        raise HTTPException(status_code=400, detail="token is invalid")    

    if existing:
        existing.verfication_states = True
        db.commit()
        return{"verification_status":f"successfully verified id {existing.customer_id} "}
    raise HTTPException(status_code=402,detail="invalid data") 


        


