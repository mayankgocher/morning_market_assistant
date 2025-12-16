from app.services.ticker_service import get_final_tickers
from app.services.market_service import build_market_context
from app.services.summary_service import generate_market_summary


def handle_user_request(user_input: str) -> dict:
    """
    Single entry point for text → intelligence
    """

    tickers = get_final_tickers(user_input)

    if not tickers:
        return {
            "summary": (
                "Some companies you mentioned are not publicly listed "
                "or do not have stock market data. "
                "Private companies and subsidiaries do not trade directly."
            ),
            "tickers": []
        }

    market_context = build_market_context(tickers)
    summary = generate_market_summary(market_context)

    return {
        "summary": summary,
        "tickers": tickers
    }
