from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import datetime

app = FastAPI(title="Compliance Service")

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
    return {"message": "Compliance Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    try:
        port = int(os.getenv("PORT", 8001))
        print(f"Health check called on port {port}")  # Debug log
        
        # Basic service checks
        response = {
            "status": "healthy",
            "service": "compliance",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "port": port,
            "host": os.getenv("HOST", "0.0.0.0")
        }
        print(f"Health check response: {response}")  # Debug log
        return response
    except Exception as e:
        error_response = {
            "status": "unhealthy",
            "error": str(e),
            "service": "compliance",
            "timestamp": datetime.datetime.now().isoformat(),
            "port": int(os.getenv("PORT", 8001))
        }
        print(f"Health check error: {error_response}")  # Debug log
        return error_response, 500

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)