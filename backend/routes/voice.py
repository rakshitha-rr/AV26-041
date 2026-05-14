"""
Voice AI Assistant Routes — STT, TTS, and Integrated Voice Assistant.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
from models.schemas import Language, VoiceAssistantResponse
from utils.speech_to_text import transcribe_audio
from utils.text_to_speech import generate_audio
from utils.sms_handler import process_chat_query

router = APIRouter(tags=["🎙️ Voice AI Assistant"])

# Directory for temp audio files
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

@router.post("/voice-input")
async def voice_to_text(
    audio: UploadFile = File(...),
    language: Language = Form(Language.ENGLISH)
):
    """Transcribe uploaded audio file to text."""
    temp_path = os.path.join(AUDIO_DIR, f"temp_{audio.filename}")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        transcription = transcribe_audio(temp_path, language.value)
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/voice-output")
async def text_to_voice(
    text: str = Form(...),
    language: Language = Form(Language.ENGLISH)
):
    """Convert text to speech and return the audio file URL."""
    try:
        filename = generate_audio(text, language.value)
        return {"audio_url": f"/api/voice/audio/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice-assistant", response_model=VoiceAssistantResponse)
async def voice_assistant(
    audio: UploadFile = File(...),
    language: Language = Form(Language.ENGLISH)
):
    """Combined Voice Assistant: Speech -> Text -> AI Logic -> Speech."""
    temp_path = os.path.join(AUDIO_DIR, f"assistant_{audio.filename}")
    try:
        # 1. Save uploaded audio
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # 2. STT: Transcribe
        transcription = transcribe_audio(temp_path, language.value)
        
        # 3. AI: Process query using existing NLP logic
        ai_result = process_chat_query(transcription, language.value)
        response_text = ai_result["response"]
        
        # 4. TTS: Generate speech response
        audio_filename = generate_audio(response_text, language.value)
        
        return VoiceAssistantResponse(
            transcription=transcription,
            text_response=response_text,
            audio_url=f"/api/voice/audio/{audio_filename}",
            detected_intent=ai_result["detected_intent"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """Serve the generated audio file."""
    file_path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(file_path, media_type="audio/mpeg")
