"""
Knowledge Garden Routes — Search and understand agricultural terms.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import Language
from utils.knowledge import get_all_farming_terms, get_term_by_id, search_terms, get_term_suggestions
from utils.text_to_speech import generate_audio

router = APIRouter(tags=["🌱 Knowledge Garden"])

@router.get("/knowledge")
async def get_term(term: str = Query(..., description="Term ID or name to search")):
    """
    Get detailed information about a specific farming term.
    """
    # First try direct ID match
    result = get_term_by_id(term)
    
    # If not found, try searching by name
    if not result:
        matches = search_terms(term)
        if matches:
            result = matches[0] # Take first match
            
    if not result:
        raise HTTPException(status_code=404, detail=f"Term '{term}' not found in Knowledge Garden.")
        
    return result

@router.get("/knowledge/search")
async def search_knowledge(query: str = Query(..., description="Search query")):
    """
    Search for terms matching the query.
    """
    matches = search_terms(query)
    return [m["name"]["en"] for m in matches]

@router.get("/knowledge/suggestions")
async def get_suggestions():
    """
    Get list of available terms.
    """
    return get_term_suggestions()

@router.get("/knowledge/voice")
async def get_term_voice(
    term_id: str = Query(..., description="ID of the term"),
    language: Language = Query(Language.ENGLISH, description="Language for speech")
):
    """
    Generate speech for a term's simple explanation.
    """
    term = get_term_by_id(term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
        
    explanation = term["simple"].get(language.value, term["simple"]["en"])
    name = term["name"].get(language.value, term["name"]["en"])
    
    full_text = f"{name}. {explanation}"
    
    try:
        filename = generate_audio(full_text, language.value)
        return {"audio_url": f"/api/voice/audio/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Keep old route for backward compatibility if needed, or redirect
@router.get("/knowledge-garden")
async def get_full_garden():
    return {
        "total": len(get_all_farming_terms()),
        "terms": get_all_farming_terms()
    }
