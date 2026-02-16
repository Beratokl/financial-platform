from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(title="User Profile Service - Demo")

# In-memory storage (no database needed)
users_db = {}

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
    created_at: str

@app.get("/")
def home():
    return {
        "service": "User Profile Service",
        "status": "running",
        "users_count": len(users_db),
        "docs": "http://localhost:8004/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "user-profile"}

@app.post("/users", response_model=UserProfileResponse)
def create_user(profile: UserProfileCreate):
    # Check if email exists
    for user in users_db.values():
        if user["email"] == profile.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = str(uuid.uuid4())
    new_user = {
        "user_id": user_id,
        "email": profile.email,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "phone": profile.phone,
        "kyc_status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    users_db[user_id] = new_user
    return new_user

@app.get("/users/{user_id}", response_model=UserProfileResponse)
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/users")
def list_users():
    return {"users": list(users_db.values()), "count": len(users_db)}

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 User Profile Service Starting (No Database Required)...")
    print("📡 Open: http://localhost:8004/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8004)
