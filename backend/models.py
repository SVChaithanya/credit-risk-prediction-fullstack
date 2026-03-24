from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from db import Base,engine


class Registration(Base):
    __tablename__ = "registration"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(Integer, unique=True, nullable=False, index=True) 
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    verify = Column(String,nullable=False)
    password = Column(String,nullable=False)
    verfication_states = Column(Boolean,nullable=False,default=False)
    registered_at = Column(DateTime, default=datetime.utcnow)




class Risk(Base):
    __tablename__ = "risk"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    customer_id = Column(Integer, unique=True, nullable=False, index=True) 
    pd = Column(Float,nullable=False)
    adjusted_pd = Column(Float,nullable=False)
    expected_loss = Column(Float,nullable=False)
    emi = Column(Float,nullable=False)
    affordability_ratio = Column(Float,nullable=False)
    decision = Column(String,nullable=False)
    risk_level = Column(String,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)



    
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_id = Column(Integer, nullable=False, index=True)

    token_hash = Column(String, nullable=False)

    expire = Column(DateTime, nullable=False)



Base.metadata.create_all(bind=engine)    