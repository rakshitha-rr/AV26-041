"""
Crop Yield Prediction Route — Core endpoint of the system.
POST /predict-yield
"""

from fastapi import APIRouter, HTTPException, Depends
from models.schemas import YieldPredictionRequest, YieldPredictionResponse, CurrentFarmer
from models.yield_model import predict_yield
from utils.interpreter import interpret_yield, get_yield_recommendations
from utils.dependencies import get_current_farmer
from db.mongo import get_db
from datetime import datetime, timezone

router = APIRouter(tags=["🌾 Yield Prediction"])


@router.post("/predict-yield", response_model=YieldPredictionResponse)
async def predict_crop_yield(
    req: YieldPredictionRequest,
    current_farmer: CurrentFarmer = Depends(get_current_farmer)
):
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

        response = YieldPredictionResponse(
            predicted_yield_tons_per_hectare=result["predicted_yield"],
            yield_category=result["category"],
            interpretation=interpretation,
            confidence_score=result["confidence"],
            recommendations=recommendations,
        )

        db = get_db()
        prediction_doc = {
            "farmer_aadhaar": current_farmer.aadhaar_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_params": req.model_dump(),
            "predicted_yield": result["predicted_yield"],
            "yield_rating": result["category"],
            "recommendations": recommendations,
            "language": req.language.value
        }
        await db.predictions.insert_one(prediction_doc)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
