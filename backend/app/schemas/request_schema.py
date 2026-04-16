from pydantic import BaseModel
from typing import Optional, Dict, Any

class MessageAnalysisRequest(BaseModel):
    message: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None

class LoginRequest(BaseModel):
    id_token: str # Firebase ID token
