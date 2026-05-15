"""
Farmer-Friendly Output Interpreter.
Converts ML outputs into simple, actionable language.
"""

from typing import List
import config


def format_number_locale(num: any, language: str) -> str:
    """Formats numbers into localized digits (Kannada/Hindi)."""
    if num is None: return ""
    s = str(num)
    digit_maps = {
        "kn": ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
        "hi": ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
        "en": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    }
    m = digit_maps.get(language, digit_maps["en"])
    return "".join(m[int(d)] if d.isdigit() else d for d in s)

def interpret_yield(predicted_yield: float, category: str, language: str = "en") -> str:
    """Convert numerical yield prediction to farmer-friendly text."""
    p_num = format_number_locale(predicted_yield, language)
    interpretations = {
        "en": {
            "very_low": f"Your expected yield of {p_num} tons/hectare is very low this season. Consider changing your farming practices or consulting an agricultural officer.",
            "low": f"Your crop is expected to give slightly below normal yield ({p_num} tons/hectare) this season. Some improvements in irrigation or fertilizer may help.",
            "average": f"Your expected yield of {p_num} tons/hectare is average for this season. You're on the right track with your farming practices.",
            "good": f"Great news! Your crop is expected to yield {p_num} tons/hectare, which is above average. Your farming practices are working well.",
            "excellent": f"Excellent! Your crop is expected to produce {p_num} tons/hectare — an outstanding yield! Continue with your current practices.",
        },
        "hi": {
            "very_low": f"आपकी अपेक्षित उपज {p_num} टन/हेक्टेयर इस मौसम में बहुत कम है। कृषि अधिकारी से सलाह लें।",
            "low": f"आपकी फसल इस मौसम में सामान्य से थोड़ी कम उपज ({p_num} टन/हेक्टेयर) दे सकती है। सिंचाई या उर्वरक में सुधार मदद कर सकता है।",
            "average": f"आपकी अपेक्षित उपज {p_num} टन/हेक्टेयर इस मौसम के लिए सामान्य है। आपकी कृषि पद्धतियां सही दिशा में हैं।",
            "good": f"अच्छी खबर! आपकी फसल {p_num} टन/हेक्टेयर उपज दे सकती है, जो औसत से ऊपर है।",
            "excellent": f"बहुत बढ़िया! आपकी फसल {p_num} टन/हेक्टेयर उत्पादन करेगी — उत्कृष्ट उपज!",
        },
        "kn": {
            "very_low": f"ನಿಮ್ಮ ನಿರೀಕ್ಷಿತ ಇಳುವರಿ {p_num} ಟನ್/ಹೆಕ್ಟೇರ್ ಈ ಋತುವಿನಲ್ಲಿ ತುಂಬಾ ಕಡಿಮೆಯಾಗಿದೆ. ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "low": f"ನಿಮ್ಮ ಬೆಳೆ ಈ ಋತುವಿನಲ್ಲಿ ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಸ್ವಲ್ಪ ಕಡಿಮೆ ಇಳುವರಿ ({p_num} ಟನ್/ಹೆಕ್ಟೇರ್) ನೀಡಬಹುದು. ನೀರಾವರಿ ಅಥವಾ ಗೊಬ್ಬರದಲ್ಲಿ ಸುಧಾರಣೆ ಸಹಾಯ ಮಾಡಬಹುದು.",
            "average": f"ನಿಮ್ಮ ನಿರೀಕ್ಷಿತ ಇಳುವರಿ {p_num} ಟನ್/ಹೆಕ್ಟೇರ್ ಈ ಋತುವಿಗೆ ಸರಾಸರಿಯಾಗಿದೆ. ನಿಮ್ಮ ಕೃಷಿ ಪದ್ಧತಿಗಳು ಸರಿಯಾದ ಹಾದಿಯಲ್ಲಿವೆ.",
            "good": f"ಶುಭ ಸುದ್ದಿ! ನಿಮ್ಮ ಬೆಳೆ {p_num} ಟನ್/ಹೆಕ್ಟೇರ್ ಇಳುವರಿ ನೀಡಬಹುದು, ಇದು ಸರಾಸರಿಗಿಂತ ಹೆಚ್ಚು.",
            "excellent": f"ಅತ್ಯುತ್ತಮ! ನಿಮ್ಮ ಬೆಳೆ {p_num} ಟನ್/ಹೆಕ್ಟೇರ್ ಉತ್ಪಾದಿಸಲಿದೆ — ಅದ್ಭುತ ಇಳುವರಿ!",
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
    language: str = "en"
) -> List[str]:
    """Generate localized actionable recommendations based on conditions."""
    recommendations = []
    
    p_ph = format_number_locale(soil_ph, language)

    recs_map = {
        "en": {
            "extension": "Consider consulting your local agricultural extension officer for personalized advice.",
            "low_rain": "Low rainfall detected. Set up drip irrigation to conserve water.",
            "high_rain": "High rainfall expected. Ensure proper drainage to prevent waterlogging.",
            "acidic": f"Soil is too acidic (pH {p_ph}). Apply agricultural lime at 2-4 tons/hectare.",
            "alkaline": f"Soil is too alkaline (pH {p_ph}). Apply gypsum to lower pH.",
            "low_moisture": "Soil moisture is low. Increase irrigation frequency.",
            "high_moisture": "Soil moisture is high. Reduce irrigation.",
            "low_fert": "Fertilizer application is low. Apply balanced NPK.",
            "high_fert": "Over-fertilization detected. Reduce fertilizer.",
            "low_irrig": "Irrigation is insufficient. Increase for optimal growth.",
            "extreme_heat": "Extreme heat detected. Use shade nets.",
            "extreme_cold": "Low temperature warning. Protect crops.",
            "optimal": "Your farming conditions look optimal. Maintain current practices."
        },
        "kn": {
            "extension": "ವೈಯಕ್ತಿಕ ಸಲಹೆಗಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "low_rain": "ಕಡಿಮೆ ಮಳೆ ಪತ್ತೆಯಾಗಿದೆ. ನೀರನ್ನು ಉಳಿಸಲು ಹನಿ ನೀರಾವರಿ ಸ್ಥಾಪಿಸಿ.",
            "high_rain": "ಹೆಚ್ಚು ಮಳೆ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ. ನೀರು ನಿಲ್ಲದಂತೆ ಸರಿಯಾದ ಚರಂಡಿ ವ್ಯವಸ್ಥೆ ಮಾಡಿ.",
            "acidic": f"ಮಣ್ಣು ತುಂಬಾ ಆಮ್ಲೀಯವಾಗಿದೆ (pH {p_ph}). ಹೆಕ್ಟೇರ್‌ಗೆ ೨-೪ ಟನ್ ಸುಣ್ಣವನ್ನು ಅನ್ವಯಿಸಿ.",
            "alkaline": f"ಮಣ್ಣು ತುಂಬಾ ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {p_ph}). pH ಕಡಿಮೆ ಮಾಡಲು ಜಿಪ್ಸಮ್ ಬಳಸಿ.",
            "low_moisture": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಕಡಿಮೆಯಾಗಿದೆ. ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ.",
            "high_moisture": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಹೆಚ್ಚಾಗಿದೆ. ನೀರಾವರಿಯನ್ನು ಕಡಿಮೆ ಮಾಡಿ.",
            "low_fert": "ಗೊಬ್ಬರ ಬಳಕೆ ಕಡಿಮೆಯಾಗಿದೆ. ಸಮತೋಲಿತ NPK ಗೊಬ್ಬರ ಬಳಸಿ.",
            "high_fert": "ಹೆಚ್ಚು ಗೊಬ್ಬರ ಪತ್ತೆಯಾಗಿದೆ. ಮಣ್ಣಿನ ಗುಣಮಟ್ಟ ಕಾಪಾಡಲು ಗೊಬ್ಬರವನ್ನು ಕಡಿಮೆ ಮಾಡಿ.",
            "low_irrig": "ನೀರಾವರಿ ಸಾಕಷ್ಟಿಲ್ಲ. ಉತ್ತಮ ಬೆಳವಣಿಗೆಗೆ ಕನಿಷ್ಠ ೫೦% ಹೆಚ್ಚಿಸಿ.",
            "extreme_heat": "ವಿಪರೀತ ಶಾಖ ಪತ್ತೆಯಾಗಿದೆ. ನೆರಳು ಬಲೆ ಬಳಸಿ ಮತ್ತು ನೀರುಣಿಸುವಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸಿ.",
            "extreme_cold": "ಕಡಿಮೆ ತಾಪಮಾನದ ಎಚ್ಚರಿಕೆ. ರಕ್ಷಣೆಗಾಗಿ ಮಲ್ಚಿಂಗ್ ಬಳಸಿ.",
            "optimal": "ನಿಮ್ಮ ಕೃಷಿ ಪರಿಸ್ಥಿತಿಗಳು ಉತ್ತಮವಾಗಿವೆ. ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ ಇದೇ ರೀತಿ ಮುಂದುವರಿಸಿ."
        },
        "hi": {
            "extension": "व्यक्तिगत सलाह के लिए अपने स्थानीय कृषि विस्तार अधिकारी से परामर्श करें।",
            "low_rain": "कम वर्षा का पता चला। पानी बचाने के लिए ड्रिप सिंचाई स्थापित करें।",
            "high_rain": "अधिक वर्षा की संभावना। जलभराव रोकने के लिए उचित जल निकासी सुनिश्चित करें।",
            "acidic": f"मिट्टी बहुत अम्लीय है (pH {p_ph})। २-४ टन/हेक्टेयर की दर से कृषि चूना लगाएं।",
            "alkaline": f"मिट्टी बहुत क्षारीय है (pH {p_ph})। pH कम करने के लिए जिप्सम लगाएं।",
            "low_moisture": "मिट्टी की नमी कम है। सिंचाई बढ़ाएं।",
            "high_moisture": "मिट्टी की नमी अधिक है। सिंचाई कम करें।",
            "low_fert": "उर्वरक का प्रयोग कम है। संतुलित NPK लगाएं।",
            "high_fert": "अधिक उर्वरक का पता चला। उर्वरक कम करें।",
            "low_irrig": "सिंचाई अपर्याप्त है। इष्टतम विकास के लिए बढ़ाएं।",
            "extreme_heat": "अत्यधिक गर्मी का पता चला। छाया जाल का प्रयोग करें।",
            "extreme_cold": "कम तापमान की चेतावनी। मल्चिंग का प्रयोग करें।",
            "optimal": "आपकी खेती की स्थिति इष्टतम दिख रही है।"
        }
    }

    l_map = recs_map.get(language, recs_map["en"])

    if category in ("very_low", "low"): recommendations.append(l_map["extension"])
    if rainfall_mm < 400: recommendations.append(l_map["low_rain"])
    elif rainfall_mm > 1500: recommendations.append(l_map["high_rain"])
    if soil_ph < 5.5: recommendations.append(l_map["acidic"])
    elif soil_ph > 8.0: recommendations.append(l_map["alkaline"])
    if soil_moisture_pct < 25: recommendations.append(l_map["low_moisture"])
    elif soil_moisture_pct > 70: recommendations.append(l_map["high_moisture"])
    if fertilizer_kg_per_hectare < 30: recommendations.append(l_map["low_fert"])
    elif fertilizer_kg_per_hectare > 250: recommendations.append(l_map["high_fert"])
    if irrigation_level_pct < 30: recommendations.append(l_map["low_irrig"])
    if temperature_c > 38: recommendations.append(l_map["extreme_heat"])
    elif temperature_c < 15: recommendations.append(l_map["extreme_cold"])
    if not recommendations: recommendations.append(l_map["optimal"])

    return recommendations


def interpret_simulation_comparison(
    original_yield: float,
    simulated_yield: float,
    change_pct: float,
    language: str = "en",
) -> str:
    """Generate farmer-friendly comparison of simulation results with localized numbers."""
    o_num = format_number_locale(original_yield, language)
    s_num = format_number_locale(simulated_yield, language)
    c_num = format_number_locale(abs(change_pct), language)
    
    if change_pct > 15: tone = "significant improvement"
    elif change_pct > 0: tone = "improvement"
    elif change_pct > -15: tone = "slight decline"
    else: tone = "significant decline"

    templates = {
        "en": f"By changing conditions, yield goes from {o_num} to {s_num} tons/hectare ({'+' if change_pct > 0 else '-'}{c_num}%). This is a {tone}.",
        "hi": f"स्थितियां बदलने से, पैदावार {o_num} से {'बढ़कर' if change_pct > 0 else 'घटकर'} {s_num} टन/हेक्टेयर ({c_num}%) हो जाती है।",
        "kn": f"ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಬದಲಾಯಿಸುವುದರಿಂದ, ಇಳುವರಿಯು {o_num} ರಿಂದ {s_num} ಟನ್/ಹೆಕ್ಟೇರ್‌ಗೆ ({'+' if change_pct > 0 else '-'}{c_num}%) {'ಹೆಚ್ಚಾಗುತ್ತದೆ' if change_pct > 0 else 'ಕಡಿಮೆಯಾಗುತ್ತದೆ'}.",
    }

    return templates.get(language, templates["en"])


def interpret_soil_quality(ph: float, moisture: float, language: str = "en") -> dict:
    """Interpret soil analysis results into localized output."""
    # Soil conditions interpretation logic...
    res = {
        "soil_quality": "Good" if language == "en" else "ಉತ್ತಮ" if language == "kn" else "अच्छा",
        "ph_status": "Optimal" if ph > 6.0 else "Acidic",
        "moisture_status": "Optimal" if moisture > 30 else "Dry",
        "suitable_crops": ["Rice", "Maize", "Ragi"] if language == "en" else ["ಭತ್ತ", "ಮೆಕ್ಕೆಜೋಳ", "ರಾಗಿ"],
        "recommendations": _get_soil_recommendations(ph, moisture, language),
    }
    return res

def _get_soil_recommendations(ph: float, moisture: float, language: str = "en") -> List[str]:
    """Generate soil improvement recommendations in local language."""
    p_num = format_number_locale(ph, language)
    if language == "kn":
        return [f"ಮಣ್ಣಿನ pH ಪರೀಕ್ಷಿಸಿ ({p_num}). ಸಾವಯವ ಗೊಬ್ಬರ ಬಳಸಿ.", "ನೀರಾವರಿ ಮಟ್ಟವನ್ನು ಪರಿಶೀಲಿಸಿ."]
    elif language == "hi":
        return [f"मिट्टी के pH की जांच करें ({p_num})। जैविक खाद का प्रयोग करें।", "सिंचाई के स्तर की जाँच करें।"]
    return [f"Test soil pH ({p_num}). Use organic manure.", "Check irrigation levels."]
