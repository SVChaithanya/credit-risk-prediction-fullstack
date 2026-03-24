from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class Register(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password : str


class Verify(BaseModel):
    token:str



class LoanRequest(BaseModel):
    loan_amnt: float = Field(ge=10000)
    annual_inc: float = Field(ge=10000)
    dti: float = Field(ge=0, le=60)
    fico_mean: float = Field(ge=300, le=850)
    int_rate: float = Field(gt=0)
    term: Literal["36 months", "60 months"]
    grade: Literal["A","B","C","D","E","F","G"]
    purpose: str  