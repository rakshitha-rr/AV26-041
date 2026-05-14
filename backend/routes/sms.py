"""
Real-world SMS and Call Integration via Twilio.
POST /send-sms, POST /webhook/sms, POST /webhook/voice
"""

from fastapi import APIRouter, HTTPException, Form, Response
from models.schemas import SMSRequest, SMSResponse, OfflineSMSRequest, OfflineSMSResponse
from utils.sms_handler import (
    send_sms, 
    parse_offline_sms, 
    format_sms_reply, 
    generate_twiml_sms_reply, 
    generate_twiml_voice_welcome_and_forward
)
from models.yield_model import predict_yield
from models.risk_model import analyze_risks, get_overall_risk_level
from utils.interpreter import interpret_soil_quality

router = APIRouter(tags=["📱 SMS & Call Center"])

# The test number provided by the user for call forwarding and manual tests
TEST_NUMBER = "+919916721196"


@router.post("/send-sms", response_model=SMSResponse)
async def send_manual_sms(req: SMSRequest):
    """
    Manually send an SMS to a farmer (used for alerts or custom messages).
    Always targets the test number if provided in the prompt for demo purposes.
    """
    target = req.phone_number if req.phone_number else TEST_NUMBER
    result = send_sms(target, req.message)
    return SMSResponse(**result)


@router.post("/webhook/sms")
async def twilio_sms_webhook(Body: str = Form(""), From: str = Form("")):
    """
    Twilio SMS Webhook — processes incoming SMS commands.
    Supported: YIELD, SOIL, RISK, HELP
    """
    parsed = parse_offline_sms(Body)
    reply = ""

    if parsed["command"] == "YIELD" and parsed["parsed"]:
        result = predict_yield(**parsed["params"])
        reply = format_sms_reply("YIELD", result)
        
    elif parsed["command"] == "SOIL" and parsed["parsed"]:
        result = interpret_soil_quality(**parsed["params"])
        reply = format_sms_reply("SOIL", result)
        
    elif parsed["command"] == "RISK" and parsed["parsed"]:
        alerts = analyze_risks(**parsed["params"])
        level = get_overall_risk_level(alerts)
        result = {"total_alerts": len(alerts), "overall_risk_level": level}
        reply = format_sms_reply("RISK", result)
        
    elif parsed["command"] == "HELP":
        reply = format_sms_reply("HELP")
        
    else:
        reply = format_sms_reply("UNKNOWN")

    # Generate TwiML response for Twilio to send back the reply SMS
    twiml_content = generate_twiml_sms_reply(reply)
    return Response(content=twiml_content, media_type="application/xml")


@router.post("/webhook/voice")
async def twilio_voice_webhook():
    """
    Twilio Voice Webhook — handles incoming calls.
    Greets the farmer and forwards to the test support number.
    """
    twiml_content = generate_twiml_voice_welcome_and_forward(TEST_NUMBER)
    return Response(content=twiml_content, media_type="application/xml")


@router.post("/offline-query", response_model=OfflineSMSResponse)
async def simulate_offline_sms(req: OfflineSMSRequest):
    """
    Simulator for testing offline commands via JSON without a real Twilio setup.
    """
    parsed = parse_offline_sms(req.sms_body)
    reply = ""
    result_data = None

    if parsed["command"] == "YIELD" and parsed["parsed"]:
        result_data = predict_yield(**parsed["params"])
        reply = format_sms_reply("YIELD", result_data)
        
    elif parsed["command"] == "SOIL" and parsed["parsed"]:
        result_data = interpret_soil_quality(**parsed["params"])
        reply = format_sms_reply("SOIL", result_data)
        
    elif parsed["command"] == "HELP":
        reply = format_sms_reply("HELP")
    else:
        reply = format_sms_reply("UNKNOWN")

    return OfflineSMSResponse(
        parsed_successfully=parsed["parsed"],
        command=parsed["command"],
        prediction_result=result_data,
        reply_message=reply
    )
