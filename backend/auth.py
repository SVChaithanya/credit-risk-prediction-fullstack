from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid, hashlib, secrets, os,logging
from fastapi import HTTPException,Depends
from models import RefreshToken
from sqlalchemy.orm import Session
from db import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordRequestForm
 

os.makedirs("logs",exist_ok=True)
logging.basicConfig(
    filename="logs/predictions.log",
    level= logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SECRET_KEY = os.getenv("SECURITY_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def generate_customer_id():
    return secrets.randbelow(10**9)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(customer_id: int):
    payload = {
        "sub": str(customer_id),
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(customer_id: int, db: Session):
    raw = str(uuid.uuid4())

    db_token = RefreshToken(
        customer_id=customer_id,
        token_hash=hash_token(raw),
        expire=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_token)
    db.commit()

    return raw


def verify_refresh_token(token: str, db: Session):
    hashed = hash_token(token)

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hashed
    ).first()

    if not db_token or db_token.expire < datetime.utcnow():
        return None

    return db_token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id = payload.get("sub")

        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return int(customer_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")