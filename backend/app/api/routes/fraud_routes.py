from fastapi import APIRouter
from pydantic import BaseModel
from app.services.firebase_service import send_push_notification

router = APIRouter()

class MessageRequest(BaseModel):
    message: str
    user_id: str
    metadata: dict = {}

@router.post("/analyze-message")
async def analyze_message(request: MessageRequest):

    # 🔥 Dummy fraud logic (replace with your ML later)
    if "click now" in request.message.lower():
        risk_result = {
            "risk_level": "fraud_high"
        }
    else:
        risk_result = {
            "risk_level": "safe"
        }

    # 🚨 SEND NOTIFICATION IF FRAUD
    if risk_result["risk_level"].startswith("fraud"):

        # ✅ Get token from request
        token = request.metadata.get("device_token")

        if token:
            send_push_notification(
                token=token,
                message_text="🚨 Fraud detected! Be careful."
            )

    return risk_result