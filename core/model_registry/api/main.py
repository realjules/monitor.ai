from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import datetime

app = FastAPI(title="Model Registry Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Model Registry Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    try:
        # Basic service checks
        return {
            "status": "healthy",
            "service": "model-registry",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "port": int(os.getenv("PORT", 8000))
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "model-registry",
            "timestamp": datetime.datetime.now().isoformat()
        }, 500

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)