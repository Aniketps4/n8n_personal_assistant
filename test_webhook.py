import requests
import os

user_message="can you tell me about black holes in 3 lines"

request_message={"message":user_message}

url= os.getenv("N8N_WEBHOOK_URL")

response=requests.post(url,json=request_message)

print(response.status_code)

print(response.json()) 