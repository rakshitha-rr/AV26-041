"""
SMS / WhatsApp Communication Route — Send, receive, and auto-reply.
POST /send-sms, POST /chat, POST /webhook/sms
"""

from fastapi import APIRouter, HTTPException, Form
from models.schemas import SMSRequest, SMSResponse, ChatQueryRequest, ChatQueryResponse
from utils.sms_handler import send_sms, process_chat_query, parse_offline_sms, format_sms_reply
from models.yield_model import predict_yield

router = APIRouter(tags=["📱 Communication"])


@router.post("/send-sms", response_model=SMSResponse)
async def send_sms_message(req: SMSRequest):
    """Send an SMS to a farmer's phone number via Twilio."""
    result = send_sms(req.phone_number, req.message)
    return SMSResponse(**result)


@router.post("/chat", response_model=ChatQueryResponse)
async def chat_with_assistant(req: ChatQueryRequest):
    """Process a natural language query from a farmer and return intelligent response."""
    try:
        result = process_chat_query(req.query, req.language.value)
        return ChatQueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/sms")
async def receive_sms_webhook(Body: str = Form(""), From: str = Form("")):
    """
    Twilio SMS webhook — receives incoming SMS, processes it, and sends auto-reply.
    Configure this URL in your Twilio phone number settings.
    """
    parsed = parse_offline_sms(Body)

    if parsed["command"] == "YIELD" and parsed["parsed"]:
        result = predict_yield(**parsed["params"])
        reply = format_sms_reply("YIELD", result)
    elif parsed["command"] == "HELP":
        reply = format_sms_reply("HELP")
    else:
        reply = format_sms_reply("UNKNOWN")

    # Send reply
    if From:
        send_sms(From, reply)

    # Return TwiML response
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply}</Message></Response>'
    from fastapi.responses import Response
    return Response(content=twiml, media_type="application/xml")
