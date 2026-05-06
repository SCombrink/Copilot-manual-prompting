import requests

# 1. The address of your local API
api_url = "http://localhost:5000/api/prompt"

# 2. The message you want to send
data_payload = {
    "prompt": "What are three fun facts about the ocean?",
    "debug": False  # Change to True if you want to watch the browser type
}

print("Sending message to your local Copilot API...")

# 3. Send the POST request
response = requests.post(api_url, json=data_payload)

# 4. Read the response
if response.status_code == 200:
    # Extract the answer from the JSON data
    answer = response.json().get("response")
    print("\nCopilot says:\n")
    print(answer)
else:
    print(f"Something went wrong! Error: {response.text}")