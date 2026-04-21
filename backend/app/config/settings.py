from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Cyber AI System"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "cyber_ai_db"
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    
    # External APIs
    VIRUSTOTAL_API_KEY: Optional[str] = None
    GOOGLE_SAFE_BROWSING_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
