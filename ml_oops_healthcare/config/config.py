from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ml_oops"
    API_PORT: int = 50711
    JWT_SECRET_KEY: str = "your-secret-key"  # Change in production
    JWT_ALGORITHM: str = "HS256"
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    
    class Config:
        env_file = ".env"

settings = Settings()