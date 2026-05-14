"""
Redis Client for Session Management
"""

import redis.asyncio as redis
from typing import Optional
import json
import config

# Global Redis client instance
redis_client: Optional[redis.Redis] = None

async def connect_redis():
    """Initialize Redis connection."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)
            await redis_client.ping()
            print("✅ Connected to Redis")
        except Exception as e:
            print(f"❌ Failed to connect to Redis: {e}")
            redis_client = None

async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        print("🛑 Redis connection closed")

def get_redis() -> redis.Redis:
    """Get the active Redis client."""
    if redis_client is None:
        raise Exception("Redis client is not initialized")
    return redis_client
