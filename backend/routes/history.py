"""
History Routes — Fetch previous predictions and alerts from MongoDB.
"""

from fastapi import APIRouter, HTTPException, Depends
from models.schemas import PredictionHistoryResponse, AlertHistoryResponse, CurrentFarmer, PredictionHistoryItem, AlertHistoryItem
from utils.dependencies import get_current_farmer
from db.mongo import get_db

router = APIRouter(tags=["📜 History"])


@router.get("/history", response_model=PredictionHistoryResponse)
async def get_prediction_history(current_farmer: CurrentFarmer = Depends(get_current_farmer)):
    """
    Fetch the last 10 yield predictions for the logged-in farmer, sorted by latest first.
    """
    try:
        db = get_db()
        cursor = db.predictions.find({"farmer_aadhaar": current_farmer.aadhaar_number}).sort("timestamp", -1).limit(10)
        docs = await cursor.to_list(length=10)
        
        predictions = []
        for doc in docs:
            doc["_id"] = str(doc["_id"])
            predictions.append(PredictionHistoryItem(**doc))
            
        return PredictionHistoryResponse(
            total=len(predictions),
            predictions=predictions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prediction history: {str(e)}")


@router.get("/alerts/history", response_model=AlertHistoryResponse)
async def get_alert_history(current_farmer: CurrentFarmer = Depends(get_current_farmer)):
    """
    Fetch the last 10 risk alerts generated for the logged-in farmer, sorted by latest first.
    """
    try:
        db = get_db()
        cursor = db.alerts.find({"farmer_aadhaar": current_farmer.aadhaar_number}).sort("timestamp", -1).limit(10)
        docs = await cursor.to_list(length=10)
        
        alerts = []
        for doc in docs:
            doc["_id"] = str(doc["_id"])
            alerts.append(AlertHistoryItem(**doc))
            
        return AlertHistoryResponse(
            total=len(alerts),
            alerts=alerts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alert history: {str(e)}")
