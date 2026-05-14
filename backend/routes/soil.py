"""
Soil Analysis Route — Analyzes soil pH and moisture for quality assessment.
POST /soil-analysis
"""

from fastapi import APIRouter, HTTPException
from models.schemas import SoilAnalysisRequest, SoilAnalysisResponse
from utils.interpreter import interpret_soil_quality

router = APIRouter(tags=["🧪 Soil Analysis"])


@router.post("/soil-analysis", response_model=SoilAnalysisResponse)
async def analyze_soil(req: SoilAnalysisRequest):
    """Analyze soil pH and moisture. Returns quality, status, recommendations, and suitable crops."""
    try:
        result = interpret_soil_quality(req.soil_ph, req.soil_moisture_pct, req.language.value)
        return SoilAnalysisResponse(
            soil_quality=result["soil_quality"],
            ph_status=result["ph_status"],
            moisture_status=result["moisture_status"],
            recommendations=result["recommendations"],
            suitable_crops=result["suitable_crops"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Soil analysis failed: {str(e)}")
