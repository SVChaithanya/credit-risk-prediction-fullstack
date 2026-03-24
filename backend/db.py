from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")  
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set!")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,          # Turn True only for debugging
    pool_size=5,
    max_overflow=10
)

# Session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()