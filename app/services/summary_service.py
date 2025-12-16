import json
from app.agents.llm_client import generate_llm_response

def generate_market_summary(market_context: dict) -> str:
    """
    Generate a concise market summary using LLM.
    """

    prompt = f"""
You are a financial market assistant.

Given the following market data in JSON format:
{json.dumps(market_context, indent=2)}

Generate a short, clear market summary covering:
- Current price and daily change for each stock
- One key news insight per stock
- Overall market tone (bullish / bearish / mixed)
- Better if reason of the market tone is included

Rules:

- Use simple language
- No markdown
- No JSON in output
"""

    return generate_llm_response(prompt)
