from fastapi import APIRouter
from app.database.mongo import get_user_history

router = APIRouter()

@router.get("/history/{user_id}")
async def fetch_user_history(user_id: str):

    history = await get_user_history(user_id)

    return {
        "user_id": user_id,
        "total_records": len(history),
        "history": history
    }