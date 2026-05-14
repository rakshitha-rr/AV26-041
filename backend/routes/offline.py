"""
Offline SMS Command Parser Route — Parse SMS text commands for yield prediction.
POST /offline-query
"""

from fastapi import APIRouter, HTTPException
from models.schemas import OfflineSMSRequest, OfflineSMSResponse
from utils.sms_handler import parse_offline_sms, format_sms_reply, send_sms
from utils.interpreter import interpret_soil_quality
from models.yield_model import predict_yield

router = APIRouter(tags=["📴 Offline Mode"])


@router.post("/offline-query", response_model=OfflineSMSResponse)
async def process_offline_sms(req: OfflineSMSRequest):
    """
    Parse an offline SMS command and return the prediction result.
    Supported commands:
      YIELD <rainfall> <temp> <ph> <moisture> <fertilizer> <irrigation>
      SOIL <ph> <moisture>
      HELP
    """
    try:
        parsed = parse_offline_sms(req.sms_body)

        if not parsed["parsed"]:
            reply = format_sms_reply("UNKNOWN")
            return OfflineSMSResponse(
                parsed_successfully=False,
                command=parsed["command"],
                reply_message=reply,
                error=parsed.get("error", "Could not parse SMS command"),
            )

        if parsed["command"] == "YIELD":
            result = predict_yield(**parsed["params"])
            reply = format_sms_reply("YIELD", result)
            return OfflineSMSResponse(
                parsed_successfully=True,
                command="YIELD",
                prediction_result=result,
                reply_message=reply,
            )

        if parsed["command"] == "SOIL":
            result = interpret_soil_quality(
                parsed["params"]["soil_ph"],
                parsed["params"]["soil_moisture_pct"],
            )
            reply = format_sms_reply("SOIL", result)
            return OfflineSMSResponse(
                parsed_successfully=True,
                command="SOIL",
                prediction_result=result,
                reply_message=reply,
            )

        if parsed["command"] == "HELP":
            reply = format_sms_reply("HELP")
            return OfflineSMSResponse(
                parsed_successfully=True,
                command="HELP",
                reply_message=reply,
            )

        reply = format_sms_reply("UNKNOWN")
        return OfflineSMSResponse(
            parsed_successfully=False,
            command="UNKNOWN",
            reply_message=reply,
            error="Unrecognized command",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Offline query failed: {str(e)}")
