"""
Knowledge Garden Route — Serve the farming dictionary.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import KnowledgeGardenResponse, Language, FarmingTerm
from utils.knowledge import get_all_farming_terms, FARMING_TERMS

router = APIRouter(tags=["🌱 Knowledge Garden"])


@router.get("/knowledge-garden", response_model=KnowledgeGardenResponse)
async def get_knowledge_garden():
    """
    Get the complete dictionary of farming terms with all translations (EN, HI, KN).
    """
    try:
        terms = get_all_farming_terms()
        return KnowledgeGardenResponse(
            total=len(terms),
            terms=[FarmingTerm(**t) for t in terms]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-garden/{term_id}", response_model=FarmingTerm)
async def get_term_details(term_id: str):
    """
    Get all translations and details for a specific farming term.
    """
    terms = get_all_farming_terms()
    term = next((t for t in terms if t["id"] == term_id), None)
    
    if not term:
        raise HTTPException(status_code=404, detail="Farming term not found")
        
    return FarmingTerm(**term)
