from app.agents.scraper_agent import extract_latest_news

tickers = ["AAPL", "TSLA", "INFY"]

for t in tickers:
    news = extract_latest_news(t)
    print(f"\n{t} news:")
    for n in news:
        print("-", n)
