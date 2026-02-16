from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI(title="Ledger Service")

ledger_db = {}

class LedgerEntryCreate(BaseModel):
    account_id: str
    transaction_type: str
    amount: float
    balance_after: float
    reference_id: str = None

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ledger"}

@app.post("/ledger/entries")
def create_entry(entry: LedgerEntryCreate):
    entry_id = str(uuid.uuid4())
    new_entry = {
        "entry_id": entry_id,
        "account_id": entry.account_id,
        "transaction_type": entry.transaction_type,
        "amount": entry.amount,
        "balance_after": entry.balance_after,
        "reference_id": entry.reference_id,
        "created_at": datetime.utcnow().isoformat()
    }
    if entry.account_id not in ledger_db:
        ledger_db[entry.account_id] = []
    ledger_db[entry.account_id].append(new_entry)
    return {"entry_id": entry_id, "status": "created"}

@app.get("/ledger/account/{account_id}")
def get_account_ledger(account_id: str):
    entries = ledger_db.get(account_id, [])
    return {"account_id": account_id, "entries": entries, "count": len(entries)}

if __name__ == "__main__":
    import uvicorn
    print("\n📒 Ledger Service Starting...")
    print("📡 Open: http://localhost:8003/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8003)
