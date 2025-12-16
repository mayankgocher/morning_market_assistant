from app.services.speech_service import speech_to_text

text = speech_to_text("sample.wav")
print("Transcribed text:", text)
