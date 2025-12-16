import whisper
import os

# Load Whisper model once (important for performance)
_whisper_model = whisper.load_model("base")

def speech_to_text(audio_file_path: str) -> str:
    """
    Converts speech audio file to text using Whisper (local).
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    result = _whisper_model.transcribe(audio_file_path)
    return result["text"].strip()
