from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Financial Platform - Quick Test")

@app.get("/")
def home():
    return {
        "status": "✅ Working!",
        "message": "Your Financial Platform is running!",
        "next_steps": [
            "Open http://localhost:8000/docs for API documentation",
            "Test the /health endpoint below"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "test-server"}

@app.post("/test")
def test_post(data: dict):
    return {"received": data, "status": "success"}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Financial Platform Test Server Starting...")
    print("="*50)
    print("\n📡 Open in browser: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
