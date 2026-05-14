"""
Crop Yield Prediction Route — Core endpoint of the system.
POST /predict-yield
"""

from fastapi import APIRouter, HTTPException
from models.schemas import YieldPredictionRequest, YieldPredictionResponse
from models.yield_model import predict_yield
from utils.interpreter import interpret_yield, get_yield_recommendations

router = APIRouter(tags=["🌾 Yield Prediction"])


@router.post("/predict-yield", response_model=YieldPredictionResponse)
async def predict_crop_yield(req: YieldPredictionRequest):
    """
    Predict crop yield based on agricultural parameters.
    Returns numerical yield, category, farmer-friendly interpretation, and recommendations.
    """
    try:
        result = predict_yield(
            rainfall_mm=req.rainfall_mm,
            temperature_c=req.temperature_c,
            soil_ph=req.soil_ph,
            soil_moisture_pct=req.soil_moisture_pct,
            fertilizer_kg_per_hectare=req.fertilizer_kg_per_hectare,
            irrigation_level_pct=req.irrigation_level_pct,
        )

        interpretation = interpret_yield(
            result["predicted_yield"], result["category"], req.language.value
        )

        recommendations = get_yield_recommendations(
            predicted_yield=result["predicted_yield"],
            category=result["category"],
            rainfall_mm=req.rainfall_mm,
            temperature_c=req.temperature_c,
            soil_ph=req.soil_ph,
            soil_moisture_pct=req.soil_moisture_pct,
            fertilizer_kg_per_hectare=req.fertilizer_kg_per_hectare,
            irrigation_level_pct=req.irrigation_level_pct,
        )

        return YieldPredictionResponse(
            predicted_yield_tons_per_hectare=result["predicted_yield"],
            yield_category=result["category"],
            interpretation=interpretation,
            confidence_score=result["confidence"],
            recommendations=recommendations,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
