"""
Risk Alert Detection Route — Analyzes conditions for drought, stress, and disease.
POST /risk-alerts
"""

from fastapi import APIRouter, HTTPException
from models.schemas import RiskAlertRequest, RiskAlertResponse, RiskAlert
from models.risk_model import analyze_risks, get_overall_risk_level
from utils.translator import translate_risk_alert, get_summary_text

router = APIRouter(tags=["⚠️ Risk Alerts"])


@router.post("/risk-alerts", response_model=RiskAlertResponse)
async def get_risk_alerts(req: RiskAlertRequest):
    """
    Analyze agricultural inputs and detect risk conditions.
    Returns categorized alerts with severity and recommendations.
    """
    try:
        alerts = analyze_risks(
            rainfall_mm=req.rainfall_mm,
            temperature_c=req.temperature_c,
            soil_ph=req.soil_ph,
            soil_moisture_pct=req.soil_moisture_pct,
            fertilizer_kg_per_hectare=req.fertilizer_kg_per_hectare,
            irrigation_level_pct=req.irrigation_level_pct,
        )

        lang = req.language.value
        translated_alerts = [translate_risk_alert(a, lang) for a in alerts]
        overall_level = get_overall_risk_level(alerts)
        summary = get_summary_text(len(alerts), overall_level, lang)

        return RiskAlertResponse(
            total_alerts=len(alerts),
            overall_risk_level=overall_level,
            alerts=[RiskAlert(**a) for a in translated_alerts],
            summary=summary,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")
