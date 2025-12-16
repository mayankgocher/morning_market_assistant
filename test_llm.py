from app.agents.llm_client import generate_llm_response

response = generate_llm_response(
    "Extract stock tickers from: Apple, Tesla and Infosys. Return only a JSON list."
)

print(response)
