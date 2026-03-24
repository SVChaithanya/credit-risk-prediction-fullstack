from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import joblib
import pandas as pd
from auth import get_current_user
from db import get_db
from schemas import LoanRequest
from models import Risk

router = APIRouter(prefix="/loan", tags=["Loan"])

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model.pkl")
features_path = os.path.join(BASE_DIR, "features.pkl")

model = joblib.load(model_path)
features = joblib.load(features_path)


@router.post("/")
def loan(
    data: LoanRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    LGD = 0.90

    PURPOSE_EMI_CAP = {
        "education": 0.50,
        "personal": 0.40,
        "small_business": 0.35,
        "credit_card": 0.30
    }

    TERM_MAP = {
        "36 months": 1.0,
        "60 months": 1.1
    }

    GRADE_MAP = {
        "A": 0.9,
        "B": 0.95,
        "C": 1.0,
        "D": 1.05,
        "E": 1.1,
        "F": 1.15,
        "G": 1.2
    }

    def calculate_emi(principal, annual_rate, months):
        r = annual_rate / (12 * 100)
        return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)

    payload = data.dict()

    # ML input
    try:
        input_df = pd.DataFrame([payload])[features]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing feature: {str(e)}")

    # Prediction
    try:
        pd_value = float(model.predict_proba(input_df)[0][1])
    except Exception:
        raise HTTPException(status_code=500, detail="Model prediction failed")

    # 🔴 FIX: safe dictionary access
    try:
        term_factor = TERM_MAP[data.term]
        grade_factor = GRADE_MAP[data.grade]
        purpose_cap = PURPOSE_EMI_CAP.get(data.purpose, 0.35)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid value: {str(e)}")

    adjusted_pd = pd_value * term_factor * grade_factor
    expected_loss = adjusted_pd * LGD * data.loan_amnt

    months = 36 if data.term == "36 months" else 60
    emi = calculate_emi(data.loan_amnt, data.int_rate, months)

    monthly_income = data.annual_inc / 12
    affordability = emi / monthly_income

    # Decision
    if affordability <= purpose_cap and adjusted_pd <= 0.30:
        decision = "accept"
        risk = "low"
    else:
        decision = "reject"
        risk = "high"

    # DB
    record = Risk(
        customer_id=user_id,  
        pd=pd_value,
        adjusted_pd=adjusted_pd,
        expected_loss=expected_loss,
        emi=emi,
        affordability_ratio=affordability,
        decision=decision,
        risk_level=risk
    )

    db.add(record)
    db.commit()

    return {
        "pd": round(pd_value, 3),
        "adjusted_pd": round(adjusted_pd, 3),
        "expected_loss": round(expected_loss, 2),
        "emi": round(emi, 2),
        "affordability_ratio": round(affordability, 2),
        "decision": decision,
        "risk_level": risk
    }
