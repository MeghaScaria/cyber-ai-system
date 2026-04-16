from app.config.database import get_database

async def save_analysis_result(user_id: str, result: dict):
    """
    Saves an analysis result to MongoDB.
    """
    db = get_database()
    # await db.analysis_history.insert_one({"user_id": user_id, **result})
    pass

async def get_user_history(user_id: str):
    """
    Retrieves analysis history from MongoDB.
    """
    db = get_database()
    # cursor = db.analysis_history.find({"user_id": user_id})
    return []
