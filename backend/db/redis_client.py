"""
Redis Client for Session Management
"""

import redis.asyncio as redis
from typing import Optional
import json
import os
import config

# Mock Redis that persists to a local JSON file to survive server reloads
class MockRedis:
    def __init__(self):
        self.file_path = "mock_redis.json"
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.data = json.load(f)
            except:
                self.data = {}
        else:
            self.data = {}

    def _save(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f)
        except:
            pass

    async def setex(self, key, ttl, value):
        self.data[key] = value
        self._save()
        return True

    async def get(self, key):
        return self.data.get(key)

    async def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
            return 1
        return 0

    async def ping(self):
        return True

    async def close(self):
        pass

mock_instance = MockRedis()
redis_client: Optional[redis.Redis] = None

async def connect_redis():
    """Initialize Redis connection."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)
            await redis_client.ping()
            print("[SUCCESS] Connected to Redis")
        except Exception as e:
            print(f"[WARNING] Redis not available, using Persistent Mock storage. Error: {e}")
            redis_client = mock_instance

async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client and redis_client != mock_instance:
        await redis_client.close()
        print("[INFO] Redis connection closed")

def get_redis() -> redis.Redis:
    """Get the active Redis client."""
    global redis_client
    if redis_client is None:
        return mock_instance
    return redis_client
