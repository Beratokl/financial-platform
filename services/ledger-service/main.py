from fastapi import FastAPI, Depends
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

app = FastAPI(title="Ledger Service")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    __table_args__ = {'schema': 'ledger'}
    
    entry_id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    reference_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

class LedgerEntryCreate(BaseModel):
    account_id: str
    transaction_type: str
    amount: float
    balance_after: float
    reference_id: str = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ledger"}

@app.post("/ledger/entries")
def create_entry(entry: LedgerEntryCreate, db: Session = Depends(get_db)):
    import uuid
    new_entry = LedgerEntry(
        entry_id=str(uuid.uuid4()),
        account_id=entry.account_id,
        transaction_type=entry.transaction_type,
        amount=entry.amount,
        balance_after=entry.balance_after,
        reference_id=entry.reference_id
    )
    db.add(new_entry)
    db.commit()
    return {"entry_id": new_entry.entry_id}

@app.get("/ledger/account/{account_id}")
def get_account_ledger(account_id: str, db: Session = Depends(get_db)):
    entries = db.query(LedgerEntry).filter(LedgerEntry.account_id == account_id).order_by(LedgerEntry.created_at.desc()).all()
    return entries
