from pydantic import BaseModel
from typing import List, Optional

class AnalysisResponse(BaseModel):
    is_fraud: bool
    fraud_score: float
    phishing_detected: bool
    anomaly_detected: bool
    risk_level: str
    confidence: str
    explanation: str
    timestamp: str
    alert: str | None = None
    timestamp: str
    confidence: str
    reasons: List[str] = []   # 🔥 ADD THIS LINE

class HistoryItem(BaseModel):
    id: str
    message: str
    timestamp: str
    result: AnalysisResponse

class RiskScoreResponse(BaseModel):
    user_id: str
    risk_score: float
    level: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str