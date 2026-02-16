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

app = FastAPI(title="Payments Service")

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {'schema': 'payments'}
    
    payment_id = Column(String, primary_key=True)
    from_account = Column(String, nullable=False)
    to_account = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")
    payment_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

class PaymentCreate(BaseModel):
    from_account: str
    to_account: str
    amount: float
    currency: str = "USD"
    payment_type: str

class PaymentResponse(BaseModel):
    payment_id: str
    from_account: str
    to_account: str
    amount: float
    currency: str
    status: str
    payment_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "payments"}

@app.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    import uuid
    new_payment = Payment(
        payment_id=str(uuid.uuid4()),
        from_account=payment.from_account,
        to_account=payment.to_account,
        amount=payment.amount,
        currency=payment.currency,
        payment_type=payment.payment_type,
        status="completed"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
