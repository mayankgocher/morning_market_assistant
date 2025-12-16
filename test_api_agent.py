from app.agents.api_agent import fetch_stock_snapshot

tickers = ["AAPL", "TSLA", "INFY"]
data = fetch_stock_snapshot(tickers)

for t, info in data.items():
    print(t, "→", info)
