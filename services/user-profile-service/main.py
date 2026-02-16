from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fintech:fintech_dev_pass@localhost:5432/fintech")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="User Profile Service")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {'schema': 'user_profile'}
    
    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    kyc_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

class UserProfileCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str = None

class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    phone: str = None
    kyc_status: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "user-profile"}

@app.post("/users", response_model=UserProfileResponse)
def create_user(profile: UserProfileCreate, db: Session = Depends(get_db)):
    import uuid
    new_user = UserProfile(
        user_id=str(uuid.uuid4()),
        email=profile.email,
        first_name=profile.first_name,
        last_name=profile.last_name,
        phone=profile.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserProfileResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
