from app.services.ticker_service import extract_tickers_from_query

query = "Give me today's update on Apple, Tesla and Infosys"
tickers = extract_tickers_from_query(query)

print("Extracted tickers:", tickers)
