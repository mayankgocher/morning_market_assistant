import time
import requests
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8"
}

def _normalize_ticker(ticker: str) -> str:
    indian_stocks = {"INFY", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK"}
    return f"{ticker}.NS" if ticker in indian_stocks else ticker


def _fetch_yahoo_rss(ticker: str, limit: int) -> list[str]:
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

    for attempt in range(3):  # retry with backoff
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            headlines = []

            for item in root.findall(".//item"):
                title = item.find("title")
                if title is not None and title.text:
                    headlines.append(title.text.strip())
                if len(headlines) >= limit:
                    break

            return headlines

        if response.status_code == 429:
            time.sleep(2 * (attempt + 1))  # backoff

    return []


def extract_latest_news(ticker_symbol: str, limit: int = 3) -> list[str]:
    """
    Fetch latest stock news using Yahoo RSS with retry & fallback.
    """

    ticker = _normalize_ticker(ticker_symbol)

    headlines = _fetch_yahoo_rss(ticker, limit)

    if headlines:
        return headlines

    # Fallback (safe, no blocking)
    return [f"No recent news available for {ticker_symbol} (rate-limited)"]
