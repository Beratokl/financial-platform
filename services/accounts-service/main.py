from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fintech:fintech_dev_pass@localhost:5432/fintech")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Accounts Service")

class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = {'schema': 'accounts'}
    
    account_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

class AccountCreate(BaseModel):
    user_id: str
    account_type: str
    currency: str = "USD"

class AccountResponse(BaseModel):
    account_id: str
    user_id: str
    account_type: str
    balance: float
    currency: str
    status: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "accounts"}

@app.post("/accounts", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    import uuid
    new_account = Account(
        account_id=str(uuid.uuid4()),
        user_id=account.user_id,
        account_type=account.account_type,
        currency=account.currency
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.get("/accounts/user/{user_id}")
def get_user_accounts(user_id: str, db: Session = Depends(get_db)):
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    return accounts
