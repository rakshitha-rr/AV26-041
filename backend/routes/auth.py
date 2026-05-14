"""
Authentication Route — Farmer Login with Aadhaar.
POST /login
"""

from fastapi import APIRouter, HTTPException
from models.schemas import FarmerLoginRequest, FarmerLoginResponse
from utils.sms_handler import send_sms

router = APIRouter(tags=["🔐 Authentication"])

@router.post("/login", response_model=FarmerLoginResponse)
async def farmer_login(req: FarmerLoginRequest):
    """
    Farmer login using Aadhaar Number.
    On successful login, sends a confirmation SMS.
    """
    try:
        # Validate Aadhaar format (basic validation: 12 digits)
        if len(req.aadhaar_number) != 12 or not req.aadhaar_number.isdigit():
            raise HTTPException(status_code=400, detail="Invalid Aadhaar Number. Must be 12 digits.")
        
        # Here we would normally verify the Aadhaar against a database or external API.
        # For this application, we simulate a successful login.
        
        sms_message = "You have successfully logined to the app and now the app name is agriintel"
        
        # Send confirmation SMS
        sms_result = send_sms(req.phone_number, sms_message)
        
        return FarmerLoginResponse(
            success=True,
            message="Login successful",
            sms_status=sms_result.get("status", "unknown")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
