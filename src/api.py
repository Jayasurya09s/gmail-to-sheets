from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.sync_service import run_email_sync

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Backend is running"}

@app.post("/sync")
def sync_emails():
    try:
        result = run_email_sync()
        return {
            "status": "success",
            "processed_emails": result.get("processed_emails", 0),
            "timestamp": result.get("timestamp")
        }
    except Exception as e:
        print(f"Sync error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "processed_emails": 0
        }
