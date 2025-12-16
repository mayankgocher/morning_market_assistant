import yfinance as yf
from app.agents.llm_client import extract_tickers_from_query

# -------------------------------------------------
# Known parent companies (VERY SMALL, SAFE LIST)
# This is NOT hardcoding everything — only parents
# -------------------------------------------------
PARENT_COMPANIES = {
    "whatsapp": "META",
    "instagram": "META",
    "facebook": "META",
    "jio": "RELIANCE",
    "reliance jio": "RELIANCE",
    "google": "GOOGL",
    "alphabet": "GOOGL",
}

# -------------------------------------------------
# Indian large-cap normalization (symbol → NSE)
# -------------------------------------------------
INDIAN_SYMBOLS = {
    "TCS": "TCS",
    "WIPRO": "WIPRO",
    "INFOSYS": "INFY",
    "HCL": "HCLTECH",
    "HDFC": "HDFCBANK",
    "TATA": "TATAMOTORS",
    "RELIANCE": "RELIANCE",
}

# -------------------------------------------------
# Market validation with NSE → BSE fallback
# -------------------------------------------------
def validate_indian_ticker(symbol: str) -> str | None:
    """
    Try NSE first, then BSE.
    Returns valid ticker or None.
    """

    # Try NSE
    nse = f"{symbol}.NS"
    try:
        if not yf.Ticker(nse).history(period="5d").empty:
            return nse
    except Exception:
        pass

    # Try BSE
    bo = f"{symbol}.BO"
    try:
        if not yf.Ticker(bo).history(period="5d").empty:
            return bo
    except Exception:
        pass

    return None


def is_valid_us_ticker(ticker: str) -> bool:
    try:
        return not yf.Ticker(ticker).history(period="5d").empty
    except Exception:
        return False


# -------------------------------------------------
# FINAL ticker resolver (THIS IS THE BRAIN)
# -------------------------------------------------
def get_final_tickers(user_text: str) -> list[str]:
    """
    Converts user language → real tradable tickers.
    """

    user_text_lower = user_text.lower()
    final_tickers = set()

    # 1️⃣ LLM extraction (first attempt)
    llm_tickers = extract_tickers_from_query(user_text)

    # 2️⃣ Validate LLM tickers
    for t in llm_tickers:
        t = t.upper()

        # US stock
        if is_valid_us_ticker(t):
            final_tickers.add(t)
            continue

        # Indian stock
        normalized = INDIAN_SYMBOLS.get(t, t)
        valid_india = validate_indian_ticker(normalized)
        if valid_india:
            final_tickers.add(valid_india)

    # 3️⃣ Parent inference (ONLY if needed)
    if not final_tickers:
        for keyword, parent in PARENT_COMPANIES.items():
            if keyword in user_text_lower:
                # Try US parent
                if is_valid_us_ticker(parent):
                    final_tickers.add(parent)
                else:
                    # Try Indian parent
                    normalized = INDIAN_SYMBOLS.get(parent, parent)
                    valid_india = validate_indian_ticker(normalized)
                    if valid_india:
                        final_tickers.add(valid_india)

    return list(final_tickers)
