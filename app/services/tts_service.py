from gtts import gTTS
import tempfile
import os

def text_to_speech(text: str) -> bytes:
    """
    Convert text to speech and return audio bytes.
    """
    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_path = tmp.name
        tts.save(audio_path)

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    os.remove(audio_path)
    return audio_bytes
