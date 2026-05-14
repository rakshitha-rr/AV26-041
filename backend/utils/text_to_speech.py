"""
Text-to-Speech Utility using gTTS (Google Text-to-Speech).
"""
from gtts import gTTS
import os
import uuid

# Ensure the temp directory exists
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio(text: str, language: str = "en") -> str:
    """
    Converts text to an MP3 audio file and returns the filename.
    """
    # gTTS uses standard language codes
    lang_map = {
        "en": "en",
        "hi": "hi",
        "kn": "kn"
    }
    tts_lang = lang_map.get(language.lower(), "en")
    
    try:
        # Generate speech
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        
        # Save to file
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts.save(filepath)
        
        return filename
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")
