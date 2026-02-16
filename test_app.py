from fastapi import FastAPI

app = FastAPI(title="Financial Platform - Test")

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Financial Platform is live!",
        "services": {
            "accounts": "http://localhost:8001/docs",
            "payments": "http://localhost:8002/docs",
            "ledger": "http://localhost:8003/docs",
            "users": "http://localhost:8004/docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
