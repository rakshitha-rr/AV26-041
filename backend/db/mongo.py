"""
MongoDB Client for Data Persistence
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import config

# Mock MongoDB for environments without a running MongoDB server
class MockCollection:
    def find(self, *args, **kwargs):
        return self
    def sort(self, *args, **kwargs):
        return self
    def limit(self, *args, **kwargs):
        return self
    async def to_list(self, length):
        return []
    async def insert_one(self, doc):
        return True

class MockDB:
    def __getattr__(self, name):
        return MockCollection()

# Global MongoDB client instance
class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None

db_instance = MongoDB()
mock_db = MockDB()

async def connect_mongo():
    """Initialize MongoDB connection."""
    if db_instance.client is None:
        try:
            # Short timeout so it doesn't hang the app
            db_instance.client = AsyncIOMotorClient(config.MONGODB_URL, serverSelectionTimeoutMS=2000)
            db_instance.db = db_instance.client[config.MONGODB_DB_NAME]
            # Verify connection
            await db_instance.client.admin.command('ping')
            print("[SUCCESS] Connected to MongoDB")
        except Exception as e:
            print(f"[WARNING] MongoDB not available, using Mock storage. Error: {e}")
            db_instance.client = None
            db_instance.db = mock_db

async def close_mongo():
    """Close MongoDB connection."""
    if db_instance.client:
        db_instance.client.close()
        print("[INFO] MongoDB connection closed")

def get_db():
    """Get the active MongoDB database instance."""
    if db_instance.db is None:
        return mock_db
    return db_instance.db
