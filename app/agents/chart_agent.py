import yfinance as yf

def fetch_price_history(ticker: str, period: str = "1mo") -> dict:
    """
    Fetch historical closing prices for a stock.
    """

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        return {"ticker": ticker, "dates": [], "prices": []}

    dates = hist.index.strftime("%Y-%m-%d").tolist()
    prices = hist["Close"].round(2).tolist()

    return {
        "ticker": ticker,
        "dates": dates,
        "prices": prices
    }
