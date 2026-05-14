"""
MongoDB Client for Data Persistence
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import config

# Global MongoDB client instance
class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None

db_instance = MongoDB()

async def connect_mongo():
    """Initialize MongoDB connection."""
    if db_instance.client is None:
        try:
            db_instance.client = AsyncIOMotorClient(config.MONGODB_URL)
            db_instance.db = db_instance.client[config.MONGODB_DB_NAME]
            # Verify connection
            await db_instance.client.admin.command('ping')
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            db_instance.client = None
            db_instance.db = None

async def close_mongo():
    """Close MongoDB connection."""
    if db_instance.client:
        db_instance.client.close()
        print("🛑 MongoDB connection closed")

def get_db():
    """Get the active MongoDB database instance."""
    if db_instance.db is None:
        raise Exception("MongoDB client is not initialized")
    return db_instance.db
