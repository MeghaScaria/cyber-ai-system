from typing import Generator
from app.config.database import get_database

async def get_db():
    db = get_database()
    try:
        yield db
    finally:
        pass # motor handles connection pooling
