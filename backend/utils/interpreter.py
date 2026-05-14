"""
Farmer-Friendly Output Interpreter.
Converts ML outputs into simple, actionable language.
"""

from typing import List
import config


def interpret_yield(predicted_yield: float, category: str, language: str = "en") -> str:
    """Convert numerical yield prediction to farmer-friendly text."""
    interpretations = {
        "en": {
            "very_low": f"Your expected yield of {predicted_yield} tons/hectare is very low this season. Consider changing your farming practices or consulting an agricultural officer.",
            "low": f"Your crop is expected to give slightly below normal yield ({predicted_yield} tons/hectare) this season. Some improvements in irrigation or fertilizer may help.",
            "average": f"Your expected yield of {predicted_yield} tons/hectare is average for this season. You're on the right track with your farming practices.",
            "good": f"Great news! Your crop is expected to yield {predicted_yield} tons/hectare, which is above average. Your farming practices are working well.",
            "excellent": f"Excellent! Your crop is expected to produce {predicted_yield} tons/hectare — an outstanding yield! Continue with your current practices.",
        },
        "hi": {
            "very_low": f"आपकी अपेक्षित उपज {predicted_yield} टन/हेक्टेयर इस मौसम में बहुत कम है। कृषि अधिकारी से सलाह लें।",
            "low": f"आपकी फसल इस मौसम में सामान्य से थोड़ी कम उपज ({predicted_yield} टन/हेक्टेयर) दे सकती है। सिंचाई या उर्वरक में सुधार मदद कर सकता है।",
            "average": f"आपकी अपेक्षित उपज {predicted_yield} टन/हेक्टेयर इस मौसम के लिए सामान्य है। आपकी कृषि पद्धतियां सही दिशा में हैं।",
            "good": f"अच्छी खबर! आपकी फसल {predicted_yield} टन/हेक्टेयर उपज दे सकती है, जो औसत से ऊपर है।",
            "excellent": f"बहुत बढ़िया! आपकी फसल {predicted_yield} टन/हेक्टेयर उत्पादन करेगी — उत्कृष्ट उपज!",
        },
        "kn": {
            "very_low": f"ನಿಮ್ಮ ನಿರೀಕ್ಷಿತ ಇಳುವರಿ {predicted_yield} ಟನ್/ಹೆಕ್ಟೇರ್ ಈ ಋತುವಿನಲ್ಲಿ ತುಂಬಾ ಕಡಿಮೆಯಾಗಿದೆ. ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "low": f"ನಿಮ್ಮ ಬೆಳೆ ಈ ಋತುವಿನಲ್ಲಿ ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಸ್ವಲ್ಪ ಕಡಿಮೆ ಇಳುವರಿ ({predicted_yield} ಟನ್/ಹೆಕ್ಟೇರ್) ನೀಡಬಹುದು. ನೀರಾವರಿ ಅಥವಾ ಗೊಬ್ಬರದಲ್ಲಿ ಸುಧಾರಣೆ ಸಹಾಯ ಮಾಡಬಹುದು.",
            "average": f"ನಿಮ್ಮ ನಿರೀಕ್ಷಿತ ಇಳುವರಿ {predicted_yield} ಟನ್/ಹೆಕ್ಟೇರ್ ಈ ಋತುವಿಗೆ ಸರಾಸರಿಯಾಗಿದೆ. ನಿಮ್ಮ ಕೃಷಿ ಪದ್ಧತಿಗಳು ಸರಿಯಾದ ಹಾದಿಯಲ್ಲಿವೆ.",
            "good": f"ಶುಭ ಸುದ್ದಿ! ನಿಮ್ಮ ಬೆಳೆ {predicted_yield} ಟನ್/ಹೆಕ್ಟೇರ್ ಇಳುವರಿ ನೀಡಬಹುದು, ಇದು ಸರಾಸರಿಗಿಂತ ಹೆಚ್ಚು.",
            "excellent": f"ಅತ್ಯುತ್ತಮ! ನಿಮ್ಮ ಬೆಳೆ {predicted_yield} ಟನ್/ಹೆಕ್ಟೇರ್ ಉತ್ಪಾದಿಸಲಿದೆ — ಅದ್ಭುತ ಇಳುವರಿ!",
        },
    }

    lang_map = interpretations.get(language, interpretations["en"])
    return lang_map.get(category, lang_map["average"])


def get_yield_recommendations(
    predicted_yield: float,
    category: str,
    rainfall_mm: float,
    temperature_c: float,
    soil_ph: float,
    soil_moisture_pct: float,
    fertilizer_kg_per_hectare: float,
    irrigation_level_pct: float,
) -> List[str]:
    """Generate actionable recommendations based on conditions."""
    recommendations = []

    # Yield-based recommendations
    if category in ("very_low", "low"):
        recommendations.append("Consider consulting your local agricultural extension officer for personalized advice.")

    # Input-specific recommendations
    if rainfall_mm < 400:
        recommendations.append("Low rainfall detected. Set up drip irrigation to conserve water and maintain crop health.")
    elif rainfall_mm > 1500:
        recommendations.append("High rainfall expected. Ensure proper drainage to prevent waterlogging.")

    if soil_ph < 5.5:
        recommendations.append(f"Soil is too acidic (pH {soil_ph}). Apply agricultural lime at 2-4 tons/hectare.")
    elif soil_ph > 8.0:
        recommendations.append(f"Soil is too alkaline (pH {soil_ph}). Apply gypsum or elemental sulfur to lower pH.")

    if soil_moisture_pct < 25:
        recommendations.append("Soil moisture is low. Increase irrigation frequency and consider mulching.")
    elif soil_moisture_pct > 70:
        recommendations.append("Soil moisture is high. Reduce irrigation to prevent root rot.")

    if fertilizer_kg_per_hectare < 30:
        recommendations.append("Fertilizer application is low. Apply balanced NPK (15:15:15) at 100-150 kg/hectare.")
    elif fertilizer_kg_per_hectare > 250:
        recommendations.append("Over-fertilization detected. Reduce fertilizer to avoid soil degradation and crop burn.")

    if irrigation_level_pct < 30:
        recommendations.append("Irrigation is insufficient. Increase to at least 50% for optimal crop growth.")

    if temperature_c > 38:
        recommendations.append("Extreme heat detected. Use shade nets and increase watering frequency.")
    elif temperature_c < 15:
        recommendations.append("Low temperature warning. Protect crops with plastic mulch or row covers.")

    # Always add a positive suggestion
    if not recommendations:
        recommendations.append("Your farming conditions look optimal. Maintain current practices for best results.")

    return recommendations


def interpret_simulation_comparison(
    original_yield: float,
    simulated_yield: float,
    change_pct: float,
    language: str = "en",
) -> str:
    """Generate farmer-friendly comparison of simulation results."""
    if change_pct > 15:
        tone = "significant improvement"
    elif change_pct > 5:
        tone = "moderate improvement"
    elif change_pct > 0:
        tone = "slight improvement"
    elif change_pct > -5:
        tone = "negligible change"
    elif change_pct > -15:
        tone = "moderate decline"
    else:
        tone = "significant decline"

    templates = {
        "en": (
            f"By changing your conditions, your yield {'increases' if change_pct > 0 else 'decreases'} "
            f"from {original_yield} to {simulated_yield} tons/hectare "
            f"({'+' if change_pct > 0 else ''}{change_pct}%). "
            f"This is a {tone} in expected production."
        ),
        "hi": (
            f"स्थितियां बदलने से आपकी उपज {original_yield} से "
            f"{'बढ़कर' if change_pct > 0 else 'घटकर'} {simulated_yield} टन/हेक्टेयर हो जाती है "
            f"({'+' if change_pct > 0 else ''}{change_pct}%)। "
            f"यह उत्पादन में {'सुधार' if change_pct > 0 else 'गिरावट'} है।"
        ),
        "kn": (
            f"ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಬದಲಾಯಿಸುವುದರಿಂದ ನಿಮ್ಮ ಇಳುವರಿ {original_yield} ರಿಂದ "
            f"{simulated_yield} ಟನ್/ಹೆಕ್ಟೇರ್‌ಗೆ {'ಹೆಚ್ಚಾಗುತ್ತದೆ' if change_pct > 0 else 'ಕಡಿಮೆಯಾಗುತ್ತದೆ'} "
            f"({'+' if change_pct > 0 else ''}{change_pct}%)."
        ),
    }

    return templates.get(language, templates["en"])


def interpret_soil_quality(ph: float, moisture: float, language: str = "en") -> dict:
    """Interpret soil analysis results."""
    # pH status
    if ph < 5.5:
        ph_status = "Acidic"
        ph_quality = "poor"
    elif ph < 6.0:
        ph_status = "Slightly Acidic"
        ph_quality = "fair"
    elif ph <= 7.5:
        ph_status = "Optimal"
        ph_quality = "good"
    elif ph <= 8.0:
        ph_status = "Slightly Alkaline"
        ph_quality = "fair"
    else:
        ph_status = "Alkaline"
        ph_quality = "poor"

    # Moisture status
    if moisture < 20:
        moisture_status = "Dry"
        moisture_quality = "poor"
    elif moisture < 35:
        moisture_status = "Slightly Dry"
        moisture_quality = "fair"
    elif moisture <= 60:
        moisture_status = "Optimal"
        moisture_quality = "good"
    elif moisture <= 75:
        moisture_status = "Moist"
        moisture_quality = "fair"
    else:
        moisture_status = "Waterlogged"
        moisture_quality = "poor"

    # Overall quality
    quality_scores = {"good": 2, "fair": 1, "poor": 0}
    avg_score = (quality_scores[ph_quality] + quality_scores[moisture_quality]) / 2

    if avg_score >= 1.5:
        overall = "Good"
    elif avg_score >= 0.5:
        overall = "Fair"
    else:
        overall = "Poor"

    # Suitable crops based on conditions
    suitable_crops = _get_suitable_crops(ph, moisture)

    # Recommendations
    recommendations = _get_soil_recommendations(ph, moisture, language)

    return {
        "soil_quality": overall,
        "ph_status": ph_status,
        "moisture_status": moisture_status,
        "suitable_crops": suitable_crops,
        "recommendations": recommendations,
    }


def _get_suitable_crops(ph: float, moisture: float) -> List[str]:
    """Determine suitable crops based on soil conditions."""
    crops = []

    if 5.5 <= ph <= 7.0 and 30 <= moisture <= 60:
        crops.extend(["Rice (Paddy)", "Ragi (Finger Millet)", "Maize"])
    if 6.0 <= ph <= 7.5 and 25 <= moisture <= 55:
        crops.extend(["Wheat", "Jowar (Sorghum)", "Groundnut"])
    if 5.5 <= ph <= 6.5 and 40 <= moisture <= 70:
        crops.extend(["Sugarcane", "Turmeric", "Ginger"])
    if 6.5 <= ph <= 8.0 and 20 <= moisture <= 50:
        crops.extend(["Cotton", "Sunflower", "Chickpea"])
    if 5.5 <= ph <= 7.0:
        crops.extend(["Vegetables", "Pulses"])
    if ph > 7.5:
        crops.extend(["Bajra (Pearl Millet)", "Barley"])

    return list(set(crops))[:6] if crops else ["Consult agricultural officer for specific recommendations"]


def _get_soil_recommendations(ph: float, moisture: float, language: str = "en") -> List[str]:
    """Generate soil improvement recommendations."""
    recs = []

    if ph < 5.5:
        recs.append("Apply agricultural lime (2-4 tons/hectare) to raise soil pH.")
    elif ph > 8.0:
        recs.append("Apply gypsum or sulfur to reduce soil alkalinity.")

    if moisture < 20:
        recs.append("Increase irrigation. Consider drip irrigation for efficiency.")
        recs.append("Apply organic mulch to retain soil moisture.")
    elif moisture > 75:
        recs.append("Improve drainage. Avoid over-irrigation.")
        recs.append("Consider raised bed farming to prevent waterlogging.")

    if 6.0 <= ph <= 7.5 and 30 <= moisture <= 60:
        recs.append("Soil conditions are optimal. Maintain current practices.")
    else:
        recs.append("Get a detailed soil test through the Soil Health Card scheme.")

    recs.append("Add organic matter (compost/farmyard manure) to improve soil structure.")

    return recs
