from app.services.market_service import build_market_context

tickers = ["AAPL", "TSLA", "INFY"]
context = build_market_context(tickers)

print(context)
