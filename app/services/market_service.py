from app.agents.api_agent import fetch_stock_snapshot
from app.agents.scraper_agent import extract_latest_news

def build_market_context(tickers: list[str]) -> dict:
    """
    Combines stock price data and news into a single context object.
    """

    stock_data = fetch_stock_snapshot(tickers)

    news_data = {}
    for ticker in tickers:
        news_data[ticker] = extract_latest_news(ticker)

    return {
        "stocks": stock_data,
        "news": news_data
    }
