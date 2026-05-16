from fastapi import APIRouter, Depends, HTTPException
from app.schemas.response_schema import RiskScoreResponse
from app.config.database import get_database

router = APIRouter()

@router.get("/risk-score", response_model=RiskScoreResponse)
async def get_risk_score(user_id: str):
    """
    Calculates the aggregated risk score for a user based on history.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Get last 20 messages for this user
        cursor = db.history.find({"user_id": user_id}).sort("timestamp", -1).limit(20)
        history = await cursor.to_list(length=20)
        
        if not history:
            return {"user_id": user_id, "risk_score": 0.0, "level": "safe"}
            
        # Calculate average score
        total_score = sum(item.get("risk_score", 0) for item in history)
        avg_score = total_score / len(history)
        
        # Normalize to 0-1 range for RiskScoreResponse if needed (assuming 0-100 input)
        risk_value = avg_score / 100.0
        
        level = "safe"
        if risk_value > 0.7:
            level = "high"
        elif risk_value > 0.4:
            level = "medium"
            
        return {
            "user_id": user_id, 
            "risk_score": round(risk_value, 2), 
            "level": level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
