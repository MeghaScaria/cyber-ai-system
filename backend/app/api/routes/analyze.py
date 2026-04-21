from fastapi import APIRouter, Depends
from app.schemas.request_schema import MessageAnalysisRequest
from app.schemas.response_schema import AnalysisResponse
from app.services import text_detection, url_detection, anomaly_detection

router = APIRouter()

@router.post("/analyze-message", response_model=AnalysisResponse)
async def analyze_message(request: MessageAnalysisRequest):
    """
    Analyzes a message for fraud, phishing URLs, and anomalies.
    """
    # Placeholder logic
    text_result = await text_detection.analyze_text(request.message)
    url_result = await url_detection.check_urls(request.message)
    anomaly_result = await anomaly_detection.check_anomaly(request.user_id, request.metadata)
    
    return {
        "is_fraud": text_result["is_fraud"],
        "fraud_score": text_result["score"],
        "phishing_detected": url_result["detected"],
        "anomaly_detected": anomaly_result["anomaly"],
        "risk_level": "low" # placeholder aggregated risk
    }
