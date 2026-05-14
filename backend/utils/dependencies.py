"""
FastAPI Dependencies for Authentication and Session Management
"""

import json
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.redis_client import get_redis
from models.schemas import CurrentFarmer

security = HTTPBearer()

async def get_current_farmer(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentFarmer:
    """
    Validate the session token against Redis and return the logged-in farmer's profile.
    Raises 401 Unauthorized if the token is invalid or expired.
    """
    token = credentials.credentials
    redis_client = get_redis()
    
    session_key = f"session:{token}"
    session_data_str = await redis_client.get(session_key)
    
    if not session_data_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        session_data = json.loads(session_data_str)
        return CurrentFarmer(
            aadhaar_number=session_data["aadhaar_number"],
            phone_number=session_data["phone_number"]
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Corrupted session data",
            headers={"WWW-Authenticate": "Bearer"},
        )
