from fastapi import APIRouter, Depends
from app.schemas.response_schema import RiskScoreResponse

router = APIRouter()

@router.get("/risk-score", response_model=RiskScoreResponse)
async def get_risk_score(user_id: str):
    """
    Calculates the aggregated risk score for a user.
    """
    return {"user_id": user_id, "risk_score": 0.05, "level": "low"}
