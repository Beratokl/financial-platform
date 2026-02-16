from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Accounts Service")

accounts_db = {}

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

@app.get("/health")
def health():
    return {"status": "healthy", "service": "accounts"}

@app.post("/accounts", response_model=AccountResponse)
def create_account(account: AccountCreate):
    account_id = str(uuid.uuid4())
    new_account = {
        "account_id": account_id,
        "user_id": account.user_id,
        "account_type": account.account_type,
        "balance": 0.0,
        "currency": account.currency,
        "status": "active"
    }
    accounts_db[account_id] = new_account
    return new_account

@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts_db[account_id]

@app.get("/accounts/user/{user_id}")
def get_user_accounts(user_id: str):
    user_accounts = [acc for acc in accounts_db.values() if acc["user_id"] == user_id]
    return {"accounts": user_accounts, "count": len(user_accounts)}

if __name__ == "__main__":
    import uvicorn
    print("\n💰 Accounts Service Starting...")
    print("📡 Open: http://localhost:8001/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)
