from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.services.firebase_service import send_push_notification
from app.services.text_detection import analyze_text
from app.services.url_detection import check_urls
from app.services.risk_engine import calculate_risk
from app.services.anomaly_detection import check_anomaly
from app.config.database import get_database

router = APIRouter()

class MessageRequest(BaseModel):
    message: str
    user_id: str
    metadata: dict = {}

@router.post("/analyze-message")
async def analyze_message(request: MessageRequest):
    """
    Analyzes a message for fraud using ML and rule-based systems.
    Connections: text_detection -> url_detection -> risk_engine -> MongoDB -> Firebase
    """
    try:
        # 1. 🔍 Run Detection Services
        text_result = await analyze_text(request.message)
        url_result = await check_urls(request.message)
        anomaly_result = await check_anomaly(request.user_id, request.metadata)

        # 2. ⚖️ Aggregate Results via Risk Engine
        risk_result = calculate_risk(text_result, url_result, anomaly_result)

        # 3. 💾 Persist to MongoDB History
        db = get_database()
        history_entry = {
            "user_id": request.user_id,
            "message": request.message,
            "risk_score": risk_result["score"],
            "risk_level": risk_result["risk_level"],
            "reasons": risk_result["reasons"],
            "timestamp": datetime.utcnow(),
            "metadata": request.metadata
        }
        
        if db is not None:
            await db.history.insert_one(history_entry)

        # 4. 🚨 Send Push Notification if High Risk
        if risk_result["risk_level"] == "fraud-high":
            token = request.metadata.get("device_token")
            if token:
                send_push_notification(
                    token=token,
                    message_text=f"🚨 Fraud Alert: {risk_result['reasons'][0] if risk_result['reasons'] else 'Suspicious message detected.'}"
                )

        return {
            "status": "success",
            "analysis": risk_result,
            "message_id": str(history_entry.get("_id", "local_only"))
        }

    except Exception as e:
        import logging
        logging.error(f"Error in analyze_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))