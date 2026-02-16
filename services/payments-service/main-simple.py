from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Payments Service")

payments_db = {}

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

@app.get("/health")
def health():
    return {"status": "healthy", "service": "payments"}

@app.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate):
    payment_id = str(uuid.uuid4())
    new_payment = {
        "payment_id": payment_id,
        "from_account": payment.from_account,
        "to_account": payment.to_account,
        "amount": payment.amount,
        "currency": payment.currency,
        "payment_type": payment.payment_type,
        "status": "completed"
    }
    payments_db[payment_id] = new_payment
    return new_payment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str):
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments_db[payment_id]

@app.get("/payments")
def list_payments():
    return {"payments": list(payments_db.values()), "count": len(payments_db)}

if __name__ == "__main__":
    import uvicorn
    print("\n💳 Payments Service Starting...")
    print("📡 Open: http://localhost:8002/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8002)
