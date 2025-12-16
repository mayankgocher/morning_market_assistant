import os
import json
import re
from groq import Groq

# ---------------------------------------
# LLM Client Setup
# ---------------------------------------
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


# ---------------------------------------
# Core LLM Call
# ---------------------------------------
def generate_llm_response(prompt: str) -> str:
    """
    Sends a prompt to the LLM and returns raw text response.
    """
    response = _client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------
# Ticker Extraction
# ---------------------------------------
def extract_tickers_from_query(user_text: str) -> list[str]:
    """
    Extract possible stock tickers from user text using LLM.
    May return empty or invalid tickers (validated later).
    """

    prompt = f"""
Extract stock tickers from the following text.

Text:
"{user_text}"

Rules:
- Return ONLY a JSON array
- Use uppercase tickers
- No explanations
- If none found, return an empty list

Example:
["AAPL", "TSLA"]
"""

    response = generate_llm_response(prompt)

    try:
        match = re.search(r"\[.*?\]", response, re.DOTALL)
        if not match:
            return []

        tickers = json.loads(match.group())
        return [t.upper() for t in tickers if isinstance(t, str)]

    except Exception:
        return []
