from fastapi import APIRouter, HTTPException
from app.config.database import get_database

router = APIRouter()

@router.post("/save-token")
async def save_token(data: dict):
    """
    Saves or updates a user's device token for push notifications in MongoDB.
    """
    user_id = data.get("user_id")
    token = data.get("device_token")

    if not user_id or not token:
        raise HTTPException(status_code=400, detail="user_id and device_token are required")

    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Upsert: Update if exists, insert if not
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"device_token": token}},
            upsert=True
        )
        return {"status": "success", "message": f"Token saved for user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))