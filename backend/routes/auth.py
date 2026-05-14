"""
Authentication Route — Farmer Login with Aadhaar.
POST /login
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid
import json
from models.schemas import FarmerLoginRequest, FarmerLoginResponse
from utils.sms_handler import send_sms
from db.redis_client import get_redis

router = APIRouter(tags=["🔐 Authentication"])
security = HTTPBearer()

@router.post("/login", response_model=FarmerLoginResponse)
async def farmer_login(req: FarmerLoginRequest):
    """
    Farmer login using Aadhaar Number.
    Generates a session token stored in Redis and sends a confirmation SMS.
    """
    try:
        if len(req.aadhaar_number) != 12 or not req.aadhaar_number.isdigit():
            raise HTTPException(status_code=400, detail="Invalid Aadhaar Number. Must be 12 digits.")
        
        # Generate session token
        session_token = str(uuid.uuid4())
        session_data = {
            "aadhaar_number": req.aadhaar_number,
            "phone_number": req.phone_number
        }
        
        # Store in Redis with 24-hour TTL (86400 seconds)
        redis_client = get_redis()
        await redis_client.setex(
            f"session:{session_token}",
            86400,
            json.dumps(session_data)
        )
        
        sms_message = "You have successfully logined to the app and now the app name is agriintel"
        sms_result = send_sms(req.phone_number, sms_message)
        
        return FarmerLoginResponse(
            success=True,
            message="Login successful",
            session_token=session_token,
            sms_status=sms_result.get("status", "unknown")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/logout")
async def farmer_logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout farmer by deleting the session token from Redis.
    """
    try:
        token = credentials.credentials
        redis_client = get_redis()
        deleted = await redis_client.delete(f"session:{token}")
        
        if deleted:
            return {"success": True, "message": "Successfully logged out"}
        else:
            raise HTTPException(status_code=400, detail="Invalid session token")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")
