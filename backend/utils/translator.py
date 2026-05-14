"""
Multilingual Translation Support.
Translates system outputs into English, Hindi, and Kannada.
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "low": {"en": "Low", "hi": "कम", "kn": "ಕಡಿಮೆ"},
    "medium": {"en": "Medium", "hi": "मध्यम", "kn": "ಮಧ್ಯಮ"},
    "high": {"en": "High", "hi": "उच्च", "kn": "ಹೆಚ್ಚು"},
    "critical": {"en": "Critical", "hi": "गंभीर", "kn": "ಗಂಭೀರ"},
    "very_low": {"en": "Very Low", "hi": "बहुत कम", "kn": "ತುಂಬಾ ಕಡಿಮೆ"},
    "average": {"en": "Average", "hi": "सामान्य", "kn": "ಸರಾಸರಿ"},
    "good": {"en": "Good", "hi": "अच्छा", "kn": "ಒಳ್ಳೆಯ"},
    "excellent": {"en": "Excellent", "hi": "उत्कृष्ट", "kn": "ಅತ್ಯುತ್ತಮ"},
    "Drought Risk": {"en": "Drought Risk", "hi": "सूखे का खतरा", "kn": "ಬರದ ಅಪಾಯ"},
    "Crop Stress": {"en": "Crop Stress", "hi": "फसल तनाव", "kn": "ಬೆಳೆ ಒತ್ತಡ"},
    "Disease Probability": {"en": "Disease Probability", "hi": "रोग की संभावना", "kn": "ರೋಗದ ಸಾಧ್ಯತೆ"},
    "Flood/Waterlogging Risk": {"en": "Flood/Waterlogging Risk", "hi": "बाढ़/जलभराव का खतरा", "kn": "ಪ್ರವಾಹ ಅಪಾಯ"},
    "Nutrient Deficiency": {"en": "Nutrient Deficiency", "hi": "पोषक तत्व की कमी", "kn": "ಪೋಷಕಾಂಶ ಕೊರತೆ"},
    "no_alerts": {
        "en": "No risk alerts detected. Your farming conditions look safe.",
        "hi": "कोई जोखिम चेतावनी नहीं। आपकी खेती की स्थिति सुरक्षित है।",
        "kn": "ಯಾವುದೇ ಅಪಾಯ ಎಚ್ಚರಿಕೆಗಳಿಲ್ಲ. ನಿಮ್ಮ ಕೃಷಿ ಸುರಕ್ಷಿತವಾಗಿದೆ.",
    },
}


def translate(key: str, language: str = "en") -> str:
    """Translate a key to the specified language."""
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(language, TRANSLATIONS[key].get("en", key))
    return key


def translate_risk_alert(alert: dict, language: str = "en") -> dict:
    """Translate a risk alert to the specified language."""
    if language == "en":
        return alert
    return {
        **alert,
        "risk_type": translate(alert["risk_type"], language),
        "risk_level": translate(alert["risk_level"], language),
    }


def get_summary_text(alerts_count: int, overall_level: str, language: str = "en") -> str:
    """Generate summary text for risk alerts."""
    if alerts_count == 0:
        return translate("no_alerts", language)
    templates = {
        "en": f"{alerts_count} risk alert(s) detected. Overall risk: {translate(overall_level, language)}.",
        "hi": f"{alerts_count} जोखिम चेतावनी। समग्र जोखिम: {translate(overall_level, 'hi')}।",
        "kn": f"{alerts_count} ಅಪಾಯ ಎಚ್ಚರಿಕೆ. ಒಟ್ಟಾರೆ ಅಪಾಯ: {translate(overall_level, 'kn')}.",
    }
    return templates.get(language, templates["en"])
