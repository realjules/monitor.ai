from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

app = FastAPI(title="ML-OOPS Healthcare Monitoring")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Prometheus metrics
Instrumentator().instrument(app).expose(app)

class PredictionLog(BaseModel):
    model_id: str
    prediction: float
    uncertainty: float
    patient_id: str
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any]
    ground_truth: Optional[float] = None

@app.post("/api/v1/log-prediction")
async def log_prediction(prediction: PredictionLog):
    try:
        # TODO: Implement storage logic
        return {"status": "success", "message": "Prediction logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    try:
        # Basic service checks
        return {
            "status": "healthy",
            "service": "healthcare",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "port": int(os.getenv("PORT", 8002))
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "healthcare",
            "timestamp": datetime.now().isoformat()
        }, 500

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)