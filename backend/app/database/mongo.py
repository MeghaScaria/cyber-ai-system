from datetime import datetime

from app.config.database import get_database
from app.database.collections import ANALYSIS_HISTORY


async def save_analysis_result(user_id: str, result: dict):

    db = get_database()

    document = {
        "user_id": user_id,
        **result,
        "timestamp": datetime.utcnow()
    }

    response = await db[ANALYSIS_HISTORY].insert_one(document)

    return str(response.inserted_id)


async def get_user_history(user_id: str):

    db = get_database()

    cursor = db[ANALYSIS_HISTORY].find(
        {"user_id": user_id}
    ).sort("timestamp", -1)

    history = []

    async for document in cursor:

        document["_id"] = str(document["_id"])

        history.append(document)

    return history