"""
SMS/WhatsApp & Chat Communication Handler.
Processes farmer queries and returns intelligent, multilingual responses.
"""

import re
from typing import Optional
import config
from models.yield_model import predict_yield
from models.risk_model import analyze_risks

def detect_intent(query: str) -> str:
    """Detect the intent of a farmer's query using multilingual keywords."""
    query = query.lower().strip()
    
    intent_keywords = {
        "yield_check": ["yield", "crop", "harvest", "production", "ugao", "fasal", "iluvari", "bele", "paida"],
        "soil": ["soil", "ph", "moisture", "mitti", "mannu", "mrunthu"],
        "disease": ["disease", "pest", "infection", "yellow", "spots", "wilt", "rog", "bimari", "roga", "keeta"],
        "scheme": ["scheme", "pm-kisan", "government", "subsidy", "yojana", "insurance", "beeme", "scheme"],
        "weather": ["weather", "rain", "rainfall", "temperature", "mausam", "barish", "male", "vathavarana"],
        "fertilizer": ["fertilizer", "urea", "npk", "manure", "compost", "khad", "gobbara", "rasagobbara"],
        "irrigation": ["irrigation", "water", "drip", "sprinkler", "sinchai", "neeru", "neeravari"],
        "greeting": ["hello", "hi", "namaste", "namaskara", "help", "sahaya"],
    }

    for intent, keywords in intent_keywords.items():
        if any(kw in query for kw in keywords):
            return intent
    return "unknown"

def process_chat_query(query: str, language: str = "en") -> dict:
    """Process a natural language farmer query and return intelligent response in specific language."""
    intent = detect_intent(query)
    lang = language.lower()

    # 7. Debug Logging
    print(f"[DEBUG] User Query: {query}")
    print(f"[DEBUG] Detected Intent: {intent}")
    print(f"[DEBUG] Language: {lang}")

    numbers = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', query)]
    response_text = ""

    # 2. Smart Routing & 4. Context Handling
    if intent == "yield_check":
        if len(numbers) >= 6:
            print("[DEBUG] API Called: predict_yield")
            try:
                res = predict_yield(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])
                val = res["predicted_yield"]
                cat = res["category"]
                
                if lang == "hi":
                    response_text = f"अनुमानित पैदावार {val} टन/हेक्टेयर ({cat}) है। सुझाव: बेहतर उत्पादन के लिए सही खाद का प्रयोग करें।"
                elif lang == "kn":
                    response_text = f"ನಿರೀಕ್ಷಿತ ಇಳುವರಿ {val} ಟನ್/ಹೆಕ್ಟೇರ್ ({cat}). ಸಲಹೆ: ಉತ್ತಮ ಇಳುವರಿಗಾಗಿ ರಸಗೊಬ್ಬರ ಬಳಸಿ."
                else:
                    response_text = f"Expected yield is {val} tons/ha ({cat}). Recommendation: Ensure optimal NPK balance for better output."
            except Exception as e:
                response_text = "Error calculating yield. Please check your numbers."
        else:
            print("[DEBUG] API Called: Prompting for Yield Context")
            if lang == "hi":
                response_text = "पैदावार जानने के लिए कृपया 6 विवरण दें: बारिश (मिमी), तापमान (C), मिट्टी pH, नमी (%), खाद (किग्रा), सिंचाई (%)."
            elif lang == "kn":
                response_text = "ಇಳುವರಿ ತಿಳಿಯಲು 6 ವಿವರ ನೀಡಿ: ಮಳೆ (mm), ತಾಪಮಾನ (C), ಮಣ್ಣಿನ pH, ತೇವಾಂಶ (%), ಗೊಬ್ಬರ (kg), ನೀರಾವರಿ (%)."
            else:
                response_text = "Please provide 6 values for Yield Prediction: Rainfall (mm), Temp (C), Soil pH, Moisture (%), Fertilizer (kg), Irrigation (%)."
                
    elif intent == "soil" or intent == "weather":
        if len(numbers) >= 6:
            print("[DEBUG] API Called: analyze_risks")
            try:
                risks = analyze_risks(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])
                if risks:
                    r = risks[0]
                    rec = r["recommendation"]
                    typ = r["risk_type"]
                    if lang == "hi":
                        response_text = f"चेतावनी: {typ}। सुझाव: {rec}"
                    elif lang == "kn":
                        response_text = f"ಎಚ್ಚರಿಕೆ: {typ}। ಸಲಹೆ: {rec}"
                    else:
                        response_text = f"Alert: {typ}. Recommendation: {rec}"
                else:
                    response_text = "Conditions look optimal! Keep up the good work."
            except Exception:
                response_text = "Error analyzing risks."
        else:
            print("[DEBUG] API Called: Prompting for Soil/Weather Context")
            if lang == "hi":
                response_text = "मिट्टी या मौसम की जांच के लिए कृपया 6 विवरण दें: बारिश, तापमान, pH, नमी, खाद, और सिंचाई."
            elif lang == "kn":
                response_text = "ಮಣ್ಣು ಅಥವಾ ಹವಾಮಾನ ಪರಿಶೀಲಿಸಲು ಮಾಹಿತಿ ನೀಡಿ: ಮಳೆ, ತಾಪಮಾನ, pH, ತೇವಾಂಶ, ಗೊಬ್ಬರ, ನೀರಾವರಿ."
            else:
                response_text = "To analyze soil or weather risks, please provide 6 values: Rainfall, Temp, pH, Moisture, Fertilizer, and Irrigation."

    elif intent == "disease":
        if lang == "hi":
            response_text = "बीमारी का अंदेशा: पीले पत्तों या धब्बों की जांच करें। सुझाव: छोटे कीटों के लिए नीम के तेल का उपयोग करें।"
        elif lang == "kn":
            response_text = "ರೋಗ: ಹಳದಿ ಎಲೆ ಅಥವಾ ಚುಕ್ಕೆಗಳನ್ನು ಗಮನಿಸಿ. ಸಲಹೆ: ಕೀಟಗಳಿಗಾಗಿ ಬೇವಿನ ಎಣ್ಣೆ ಬಳಸಿ."
        else:
            response_text = "Disease check: Look for yellow leaves or spots. Recommendation: Use Neem oil for minor pests."
            
    elif intent == "scheme":
        if lang == "hi":
            response_text = "योजना: PM-KISAN सालाना ₹6000 देता है। सुझाव: पंजीकरण के लिए अपनी ग्राम पंचायत से संपर्क करें।"
        elif lang == "kn":
            response_text = "ಯೋಜನೆ: PM-KISAN ವರ್ಷಕ್ಕೆ ₹6000 ನೀಡುತ್ತದೆ. ಸಲಹೆ: ನೋಂದಣಿಗಾಗಿ ಗ್ರಾಮ ಪಂಚಾಯತ್ ಸಂಪರ್ಕಿಸಿ."
        else:
            response_text = "Schemes: PM-KISAN provides ₹6000/year. Recommendation: Contact your Gram Panchayat for enrollment."
            
    elif intent == "greeting":
        if lang == "hi":
            response_text = "नमस्ते! 🌾 मैं एग्री-इंटेल एआई हूँ। मैं पैदावार, मिट्टी और योजनाओं में मदद कर सकता हूँ। मैं क्या करूँ?"
        elif lang == "kn":
            response_text = "ನಮಸ್ಕಾರ! 🌾 ನಾನು ಅಗ್ರಿ-ಇಂಟೆಲ್ ಎಐ. ಇಳುವರಿ, ಮಣ್ಣು ಮತ್ತು ಯೋಜನೆಗಳ ಬಗ್ಗೆ ನಾನು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ನಾನು ಏನು ಮಾಡಲಿ?"
        else:
            response_text = "Namaskara! 🌾 I am AgriIntel AI. I can help with Yield, Soil, Weather, and Schemes. How can I assist you?"
            
    else:
        # 3. Fallback Response
        print("[DEBUG] API Called: Fallback Triggered")
        if lang == "hi":
            response_text = "मुझे समझ नहीं आया। कृपया पैदावार, मिट्टी, या फसलों के बारे में पूछें।"
        elif lang == "kn":
            response_text = "ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಇಳುವರಿ, ಮಣ್ಣು ಅಥವಾ ಬೆಳೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ."
        else:
            response_text = "I didn’t understand. Please ask about yield, soil, or crops."

    return {
        "query": query,
        "response": response_text,
        "detected_intent": intent,
        "suggestions": ["Ask about Yield", "Check Soil Health", "Government Schemes"]
    }

def send_sms(phone_number: str, message: str) -> dict:
    """Send SMS via Twilio (Simulated if credentials missing)."""
    if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN:
        try:
            from twilio.rest import Client
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            msg = client.messages.create(body=message, from_=config.TWILIO_PHONE_NUMBER, to=phone_number)
            return {"success": True, "message_sid": msg.sid}
        except Exception as e:
            return {"success": False, "detail": str(e)}
    return {"success": True, "detail": "[DEMO] SMS Sent"}

def parse_offline_sms(sms_body: str) -> dict:
    """Parse offline SMS command for yield prediction, soil analysis, or risk alerts."""
    sms_body = sms_body.strip().upper()
    yield_pattern = r'^YIELD\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)$'
    match = re.match(yield_pattern, sms_body)
    if match:
        return {
            "command": "YIELD", "parsed": True,
            "params": {
                "rainfall_mm": float(match.group(1)), "temperature_c": float(match.group(2)),
                "soil_ph": float(match.group(3)), "soil_moisture_pct": float(match.group(4)),
                "fertilizer_kg_per_hectare": float(match.group(5)), "irrigation_level_pct": float(match.group(6)),
            },
        }
    if sms_body in ("HELP", "MENU"): return {"command": "HELP", "parsed": True, "params": {}}
    return {"command": "UNKNOWN", "parsed": False, "params": {}}

def format_sms_reply(command: str, result: Optional[dict] = None) -> str:
    """Format prediction result as SMS-friendly text."""
    if command == "HELP":
        return "AgriIntel SMS: YIELD <rain> <temp> <ph> <moist> <fert> <irr>\nCALL 9916721196 for Support"
    if command == "YIELD" and result:
        y = result.get("predicted_yield_tons_per_hectare", 0)
        return f"AgriIntel Yield: {y} tons/hectare. Reply HELP for more."
    return "Invalid command. Reply HELP for commands."

def generate_twiml_sms_reply(message: str) -> str:
    from twilio.twiml.messaging_response import MessagingResponse
    response = MessagingResponse()
    response.message(message)
    return str(response)

def generate_twiml_voice_welcome_and_forward(forward_to: str) -> str:
    from twilio.twiml.voice_response import VoiceResponse
    response = VoiceResponse()
    response.say("Welcome to AgriIntel. Connecting you to support.")
    response.dial(forward_to)
    return str(response)
