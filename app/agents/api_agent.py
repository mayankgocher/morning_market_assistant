import yfinance as yf

def fetch_stock_snapshot(tickers: list[str]) -> dict:
    market_data = {}

    for ticker_symbol in tickers:
        try:
            ticker = yf.Ticker(ticker_symbol)

            # Fetch more days to avoid empty data issues
            hist = ticker.history(period="5d", interval="1d")

            if hist.empty or len(hist["Close"].dropna()) < 2:
                market_data[ticker_symbol] = {
                    "error": "Market data not available"
                }
                continue

            closes = hist["Close"].dropna()
            latest_close = float(closes.iloc[-1])
            previous_close = float(closes.iloc[-2])
            change = round(latest_close - previous_close, 2)

            market_data[ticker_symbol] = {
                "latest_close": latest_close,
                "change": change,
                "currency": ticker.fast_info.get("currency", "N/A"),
                "exchange": ticker.fast_info.get("exchange", "N/A")
            }

        except Exception as e:
            market_data[ticker_symbol] = {
                "error": str(e)
            }

    return market_data
