from fastapi import APIRouter
from pydantic import BaseModel
from app.services.sms_ml_service import predict_sms

router = APIRouter()

class SMSRequest(BaseModel):
    text: str


@router.post("/analyze-sms")
async def analyze_sms(data: SMSRequest):
    return predict_sms(data.text)