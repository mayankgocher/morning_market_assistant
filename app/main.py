from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
import base64

from app.controllers.request_controller import handle_user_request
from app.services.speech_service import speech_to_text
from app.services.tts_service import text_to_speech
from app.agents.chart_agent import fetch_price_history

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------
app = FastAPI(title="Morning Market Assistant")

# -------------------------------------------------
# Serve Frontend (UI)
# -------------------------------------------------
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/ui")
def serve_ui():
    """
    Serves the user-friendly frontend UI.
    """
    return FileResponse("frontend/index.html")

# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------------------------------------
# Request Model for Text Input
# -------------------------------------------------
class TextRequest(BaseModel):
    query: str

# -------------------------------------------------
# TEXT INPUT → SUMMARY + TICKERS + VOICE
# -------------------------------------------------
@app.post("/text/query")
def text_query(req: TextRequest):
    """
    Accepts text input and returns:
    - market summary
    - detected tickers
    - voice response (base64)
    """

    result = handle_user_request(req.query)

    response_text = result["summary"]
    tickers = result["tickers"]

    # Text → Speech
    audio_bytes = text_to_speech(response_text)
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "response": response_text,
        "tickers": tickers,
        "audio_b64": audio_b64
    }

# -------------------------------------------------
# VOICE INPUT → SUMMARY + TICKERS + VOICE
# -------------------------------------------------
@app.post("/voice/query")
async def voice_query(file: UploadFile = File(...)):
    """
    Accepts voice input, transcribes it, generates summary,
    returns summary, tickers, and spoken response.
    """

    suffix = os.path.splitext(file.filename)[-1] or ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        audio_path = tmp.name
        tmp.write(await file.read())

    try:
        # Speech → Text (Whisper)
        transcribed_text = speech_to_text(audio_path)

        # Text → Market Summary + Tickers
        result = handle_user_request(transcribed_text)

        response_text = result["summary"]
        tickers = result["tickers"]

        # Text → Speech
        audio_bytes = text_to_speech(response_text)
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "transcribed_text": transcribed_text,
            "response": response_text,
            "tickers": tickers,
            "audio_b64": audio_b64
        }

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

# -------------------------------------------------
# 📊 CHART DATA ENDPOINT
# -------------------------------------------------
@app.get("/chart-data/{ticker}")
def chart_data(ticker: str):
    """
    Returns historical price data for chart visualization.
    """
    return fetch_price_history(ticker)
