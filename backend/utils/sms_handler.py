"""
SMS/WhatsApp Communication Handler.
Integrates with Twilio for sending/receiving SMS and processing farmer queries.
"""

import re
from typing import Optional
import config


def send_sms(phone_number: str, message: str) -> dict:
    """Send SMS via Twilio. Returns mock response if Twilio not configured."""
    if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN:
        try:
            from twilio.rest import Client
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            msg = client.messages.create(
                body=message,
                from_=config.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )
            return {"success": True, "message_sid": msg.sid, "status": msg.status, "detail": "SMS sent via Twilio"}
        except Exception as e:
            return {"success": False, "message_sid": "", "status": "failed", "detail": str(e)}
    else:
        return {
            "success": True,
            "message_sid": "DEMO_MSG_001",
            "status": "queued",
            "detail": f"[DEMO MODE] SMS to {phone_number}: {message[:80]}...",
        }


def process_chat_query(query: str, language: str = "en") -> dict:
    """Process a natural language farmer query and return intelligent response."""
    query_lower = query.lower().strip()
    intent = detect_intent(query_lower)

    responses = {
        "yield_check": {
            "response": "To check your expected crop yield, please provide: rainfall (mm), temperature (°C), soil pH, soil moisture (%), fertilizer usage (kg/hectare), and irrigation level (%). You can use our /predict-yield endpoint or send an SMS like: YIELD 750 28 6.5 45 80 60",
            "suggestions": ["Send 'YIELD 750 28 6.5 45 80 60' via SMS", "Use the yield prediction tool on the app"],
        },
        "weather": {
            "response": "Current weather conditions affect your crop significantly. High temperatures above 38°C can cause crop stress. Low rainfall below 300mm increases drought risk. Monitor local weather forecasts and adjust irrigation accordingly.",
            "suggestions": ["Check risk alerts for your area", "Set up irrigation schedule"],
        },
        "soil": {
            "response": "Soil health is crucial for good yields. Optimal pH is 6.0-7.5 and moisture should be 30-60%. Get your soil tested through the Soil Health Card Scheme (free). Use our /soil-analysis endpoint for instant analysis.",
            "suggestions": ["Test your soil pH and moisture", "Apply for Soil Health Card"],
        },
        "disease": {
            "response": "Common crop diseases in Karnataka include blast (rice), rust (wheat), and wilt (pulses). Watch for yellowing leaves, spots, or wilting. Send a photo of the affected crop to our /disease-detection endpoint for diagnosis.",
            "suggestions": ["Upload crop photo for diagnosis", "Apply preventive fungicide"],
        },
        "scheme": {
            "response": "Several government schemes can help you: PM-KISAN (₹6,000/year), PMFBY (crop insurance), Soil Health Card (free soil testing), and PMKSY (irrigation subsidies). Use /check-eligibility to see which schemes you qualify for.",
            "suggestions": ["Check PM-KISAN eligibility", "Apply for crop insurance"],
        },
        "fertilizer": {
            "response": "Balanced fertilizer application is key. For most crops, apply NPK (15:15:15) at 100-150 kg/hectare. Avoid over-fertilization (>250 kg/hectare) as it can damage crops and soil. Consider organic alternatives like vermicompost.",
            "suggestions": ["Get soil test for precise recommendation", "Try organic fertilizers"],
        },
        "irrigation": {
            "response": "Drip irrigation saves 30-50% water compared to flood irrigation. Maintain irrigation at 40-70% for most crops. During dry spells, increase frequency but avoid waterlogging. PMKSY scheme offers subsidies for micro-irrigation setup.",
            "suggestions": ["Apply for PMKSY irrigation subsidy", "Switch to drip irrigation"],
        },
        "greeting": {
            "response": "Namaskara! 🌾 Welcome to AgriAssist AI. I can help you with crop yield predictions, soil analysis, disease detection, risk alerts, and government scheme information. How can I help you today?",
            "suggestions": ["Check crop yield prediction", "Analyze soil health", "View risk alerts"],
        },
        "unknown": {
            "response": "I can help you with: 1) Crop yield predictions 2) Soil analysis 3) Disease detection 4) Risk alerts 5) Government schemes 6) Irrigation & fertilizer advice. Please ask about any of these topics!",
            "suggestions": ["Predict my crop yield", "Analyze my soil", "Check government schemes"],
        },
    }

    result = responses.get(intent, responses["unknown"])
    return {
        "query": query,
        "response": result["response"],
        "detected_intent": intent,
        "suggestions": result["suggestions"],
    }


def detect_intent(query: str) -> str:
    """Detect the intent of a farmer's query."""
    intent_keywords = {
        "yield_check": ["yield", "crop", "harvest", "production", "how is my crop", "ugao", "fasal"],
        "weather": ["weather", "rain", "rainfall", "temperature", "mausam", "barish"],
        "soil": ["soil", "ph", "moisture", "mitti", "mannu"],
        "disease": ["disease", "pest", "infection", "yellow", "spots", "wilt", "rog", "bimari"],
        "scheme": ["scheme", "pm-kisan", "government", "subsidy", "yojana", "insurance"],
        "fertilizer": ["fertilizer", "urea", "npk", "manure", "compost", "khad", "gobbara"],
        "irrigation": ["irrigation", "water", "drip", "sprinkler", "sinchai", "neeru"],
        "greeting": ["hello", "hi", "namaste", "namaskara", "help"],
    }

    for intent, keywords in intent_keywords.items():
        if any(kw in query for kw in keywords):
            return intent
    return "unknown"


def parse_offline_sms(sms_body: str) -> dict:
    """
    Parse offline SMS command for yield prediction.
    Format: YIELD <rainfall> <temp> <ph> <moisture> <fertilizer> <irrigation>
    Example: YIELD 750 28 6.5 45 80 60
    """
    sms_body = sms_body.strip().upper()

    # Parse YIELD command
    yield_pattern = r'^YIELD\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)$'
    match = re.match(yield_pattern, sms_body)

    if match:
        return {
            "command": "YIELD",
            "parsed": True,
            "params": {
                "rainfall_mm": float(match.group(1)),
                "temperature_c": float(match.group(2)),
                "soil_ph": float(match.group(3)),
                "soil_moisture_pct": float(match.group(4)),
                "fertilizer_kg_per_hectare": float(match.group(5)),
                "irrigation_level_pct": float(match.group(6)),
            },
        }

    # Parse SOIL command: SOIL <ph> <moisture>
    soil_pattern = r'^SOIL\s+([\d.]+)\s+([\d.]+)$'
    match = re.match(soil_pattern, sms_body)
    if match:
        return {
            "command": "SOIL",
            "parsed": True,
            "params": {"soil_ph": float(match.group(1)), "soil_moisture_pct": float(match.group(2))},
        }

    # Parse HELP command
    if sms_body in ("HELP", "MENU"):
        return {
            "command": "HELP",
            "parsed": True,
            "params": {},
        }

    return {"command": "UNKNOWN", "parsed": False, "params": {}, "error": f"Could not parse: {sms_body}"}


def format_sms_reply(command: str, result: Optional[dict] = None) -> str:
    """Format prediction result as SMS-friendly text."""
    if command == "HELP":
        return (
            "AgriAssist SMS Commands:\n"
            "YIELD <rain> <temp> <ph> <moist> <fert> <irr>\n"
            "SOIL <ph> <moisture>\n"
            "HELP - Show this menu\n"
            "Example: YIELD 750 28 6.5 45 80 60"
        )
    if command == "YIELD" and result:
        y = result.get("predicted_yield", 0)
        cat = result.get("category", "average")
        return f"AgriAssist Yield Result:\nYield: {y} tons/hectare\nRating: {cat.upper()}\nReply HELP for more."
    if command == "SOIL" and result:
        return f"Soil Analysis:\nQuality: {result.get('soil_quality', 'N/A')}\npH: {result.get('ph_status', 'N/A')}\nMoisture: {result.get('moisture_status', 'N/A')}"
    return "Invalid command. Reply HELP for available commands."
