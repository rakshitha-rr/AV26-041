"""
Speech-to-Text Utility using SpeechRecognition.
"""
import speech_recognition as sr
import os

def map_language_code(lang: str) -> str:
    """Map our application's language code to SpeechRecognition's expected format."""
    mapping = {
        "en": "en-IN",
        "hi": "hi-IN",
        "kn": "kn-IN"
    }
    return mapping.get(lang.lower(), "en-IN")

def transcribe_audio(file_path: str, language: str = "en") -> str:
    """
    Transcribes a WAV/FLAC audio file into text using Google Web Speech API.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at {file_path}")
        
    recognizer = sr.Recognizer()
    lang_code = map_language_code(language)
    
    try:
        with sr.AudioFile(file_path) as source:
            # Read the entire audio file
            audio_data = recognizer.record(source)
            
            # Use Google Speech Recognition
            text = recognizer.recognize_google(audio_data, language=lang_code)
            return text
    except sr.UnknownValueError:
        raise ValueError("Speech Recognition could not understand the audio. Please speak clearly.")
    except sr.RequestError as e:
        raise ConnectionError(f"Could not request results from Speech Recognition service; {e}")
    except Exception as e:
        raise Exception(f"Error processing audio: {str(e)}")
