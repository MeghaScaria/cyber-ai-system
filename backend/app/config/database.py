from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
import logging

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]
    logging.info("Connected to MongoDB")

async def close_mongo_connection():
    db_instance.client.close()
    logging.info("Closed MongoDB connection")

def get_database():
    return db_instance.db
