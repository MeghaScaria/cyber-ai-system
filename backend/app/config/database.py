from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
import logging

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()


async def connect_to_mongo():
    try:
        db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)

        # 🔥 VERIFY CONNECTION
        await db_instance.client.admin.command("ping")

        db_instance.db = db_instance.client[settings.DATABASE_NAME]

        print("✅ Connected to MongoDB Atlas")

    except Exception as e:
        print("❌ MongoDB Connection Error:", e)


async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("🔌 MongoDB connection closed")


def get_database():
    return db_instance.db