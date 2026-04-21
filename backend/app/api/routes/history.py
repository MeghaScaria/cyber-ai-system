from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.response_schema import HistoryItem
from app.config.database import get_database

router = APIRouter()

@router.get("/history", response_model=List[dict])
async def get_history(user_id: str):
    """
    Retrieves analysis history for a specific user from MongoDB.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Fetching last 50 items for the user
        cursor = db.history.find({"user_id": user_id}).sort("timestamp", -1).limit(50)
        history = await cursor.to_list(length=50)
        
        # Convert ObjectId to string for JSON serialization
        for item in history:
            item["id"] = str(item["_id"])
            del item["_id"]
            
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
