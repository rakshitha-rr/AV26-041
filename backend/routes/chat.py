"""
Chatbot Route — Handles natural language text queries.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import ChatQueryRequest, ChatQueryResponse
from utils.sms_handler import process_chat_query

router = APIRouter(tags=["🤖 AI Advisor"])

@router.post("/chat", response_model=ChatQueryResponse)
async def chat_query(req: ChatQueryRequest):
    """
    Handle natural language farming questions using the multilingual brain.
    """
    try:
        # Use the centralized intelligent handler
        result = process_chat_query(req.query, req.language.value if hasattr(req, 'language') else 'en')
        
        return ChatQueryResponse(
            query=req.query,
            response=result["response"],
            detected_intent=result["detected_intent"],
            suggestions=result["suggestions"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
