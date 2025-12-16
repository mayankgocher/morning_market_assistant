from app.controllers.request_controller import handle_user_request

query = "Give me today's market update for Apple, Tesla and Infosys"

result = handle_user_request(query)
print(result)
