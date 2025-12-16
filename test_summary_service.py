from app.services.market_service import build_market_context
from app.services.summary_service import generate_market_summary

tickers = ["AAPL", "TSLA", "INFY"]
context = build_market_context(tickers)

summary = generate_market_summary(context)
print(summary)
