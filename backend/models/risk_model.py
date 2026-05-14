"""
Risk Detection Model for agricultural alerts.
Analyzes input conditions to detect drought, crop stress, and disease risks.
"""

from typing import List
import config


def analyze_risks(
    rainfall_mm: float,
    temperature_c: float,
    soil_ph: float,
    soil_moisture_pct: float,
    fertilizer_kg_per_hectare: float,
    irrigation_level_pct: float,
) -> List[dict]:
    """
    Analyze agricultural inputs and detect risk conditions.
    Returns a list of risk alerts with severity and recommendations.
    """
    alerts = []
    thresholds = config.RISK_THRESHOLDS

    # ─── 1. Drought Risk ─────────────────────────────────────────
    drought = thresholds["drought"]
    drought_score = 0

    if rainfall_mm < drought["rainfall_below"]:
        drought_score += 2
    if rainfall_mm < drought["rainfall_below"] * 0.5:
        drought_score += 1
    if temperature_c > drought["temperature_above"]:
        drought_score += 2
    if soil_moisture_pct < 20:
        drought_score += 2
    if irrigation_level_pct < 30:
        drought_score += 1

    if drought_score >= 4:
        level = "critical"
        msg = "Severe drought conditions detected. Immediate irrigation required."
    elif drought_score >= 2:
        level = "high"
        msg = "High drought risk in the coming days. Consider increasing irrigation."
    elif drought_score >= 1:
        level = "medium"
        msg = "Moderate drought risk. Monitor soil moisture levels closely."
    else:
        level = None
        msg = None

    if level:
        alerts.append({
            "risk_type": "Drought Risk",
            "risk_level": level,
            "message": msg,
            "recommendation": _get_drought_recommendation(drought_score, irrigation_level_pct),
            "icon": "🏜️",
        })

    # ─── 2. Crop Stress ──────────────────────────────────────────
    stress = thresholds["crop_stress"]
    stress_score = 0

    if soil_ph < stress["ph_low"] or soil_ph > stress["ph_high"]:
        stress_score += 2
    if soil_moisture_pct < stress["moisture_below"]:
        stress_score += 2
    if temperature_c > stress["temperature_above"]:
        stress_score += 2
    if fertilizer_kg_per_hectare > 250:
        stress_score += 1  # Over-fertilization stress

    if stress_score >= 4:
        level = "critical"
        msg = "Critical crop stress detected. Multiple stress factors present."
    elif stress_score >= 2:
        level = "high"
        msg = "Crop stress detected. Take corrective measures soon."
    elif stress_score >= 1:
        level = "medium"
        msg = "Mild crop stress indicators present. Monitor conditions."
    else:
        level = None
        msg = None

    if level:
        alerts.append({
            "risk_type": "Crop Stress",
            "risk_level": level,
            "message": msg,
            "recommendation": _get_stress_recommendation(soil_ph, soil_moisture_pct, temperature_c),
            "icon": "🌿",
        })

    # ─── 3. Disease Probability ──────────────────────────────────
    disease = thresholds["disease"]
    disease_score = 0

    if soil_moisture_pct > disease["moisture_above"]:
        disease_score += 2
    temp_low, temp_high = disease["temperature_range"]
    if temp_low <= temperature_c <= temp_high and soil_moisture_pct > 50:
        disease_score += 2
    if soil_ph < 5.5 or soil_ph > 8.0:
        disease_score += 1

    if disease_score >= 4:
        level = "high"
        msg = "High disease probability. Warm and humid conditions favor fungal/bacterial growth."
    elif disease_score >= 2:
        level = "medium"
        msg = "Moderate disease risk. Watch for early symptoms on leaves and stems."
    elif disease_score >= 1:
        level = "low"
        msg = "Low disease risk, but conditions could worsen. Maintain field hygiene."
    else:
        level = None
        msg = None

    if level:
        alerts.append({
            "risk_type": "Disease Probability",
            "risk_level": level,
            "message": msg,
            "recommendation": _get_disease_recommendation(soil_moisture_pct, temperature_c),
            "icon": "🦠",
        })

    # ─── 4. Flood Risk ───────────────────────────────────────────
    if rainfall_mm > 1500:
        flood_level = "critical" if rainfall_mm > 2000 else "high"
        alerts.append({
            "risk_type": "Flood/Waterlogging Risk",
            "risk_level": flood_level,
            "message": f"Excessive rainfall ({rainfall_mm}mm) may cause waterlogging and root damage.",
            "recommendation": "Ensure proper drainage systems. Raise planting beds if possible. Avoid low-lying areas.",
            "icon": "🌊",
        })

    # ─── 5. Nutrient Deficiency ──────────────────────────────────
    if fertilizer_kg_per_hectare < 20 and soil_ph < 5.5:
        alerts.append({
            "risk_type": "Nutrient Deficiency",
            "risk_level": "medium",
            "message": "Low fertilizer usage combined with acidic soil may lead to nutrient deficiency.",
            "recommendation": "Apply balanced NPK fertilizer. Consider lime application to correct soil pH.",
            "icon": "⚗️",
        })

    return alerts


def get_overall_risk_level(alerts: List[dict]) -> str:
    """Determine overall risk level from all alerts."""
    if not alerts:
        return "low"

    levels = [a["risk_level"] for a in alerts]
    if "critical" in levels:
        return "critical"
    if "high" in levels:
        return "high"
    if "medium" in levels:
        return "medium"
    return "low"


def _get_drought_recommendation(score: int, irrigation: float) -> str:
    if score >= 4:
        return (
            "Activate emergency irrigation immediately. "
            "Apply mulch to retain soil moisture. "
            "Consider drought-resistant crop varieties for next season."
        )
    if irrigation < 40:
        return (
            "Increase irrigation to at least 50%. "
            "Use drip irrigation for water efficiency. "
            "Apply organic mulch around plant bases."
        )
    return "Monitor weather forecasts. Keep irrigation systems ready for deployment."


def _get_stress_recommendation(ph: float, moisture: float, temp: float) -> str:
    recs = []
    if ph < 5.0:
        recs.append("Apply agricultural lime to raise soil pH.")
    elif ph > 8.5:
        recs.append("Apply gypsum or sulfur to lower soil pH.")
    if moisture < 20:
        recs.append("Increase irrigation immediately.")
    if temp > 38:
        recs.append("Use shade nets to protect crops from extreme heat.")
    return " ".join(recs) if recs else "Continue monitoring crop health indicators."


def _get_disease_recommendation(moisture: float, temp: float) -> str:
    recs = []
    if moisture > 65:
        recs.append("Improve drainage and reduce irrigation frequency.")
    if 22 <= temp <= 32:
        recs.append("Apply preventive fungicide spray.")
    recs.append("Remove infected plant debris. Maintain proper crop spacing for air circulation.")
    return " ".join(recs)
