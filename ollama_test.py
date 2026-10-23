
import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "llama3.2",
    "messages": [
        {
            "role": "user",
            "content": "Explain artificial intelligence in simple words."
        }
    ],
    "stream": False
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=120
    )
    response.raise_for_status()

    result = response.json()

    print("Local Ollama connection successful!")
    print("AI response:", result["message"]["content"])

except requests.RequestException as error:
    print("Could not connect to Ollama.")
    print("Check that Ollama is running and the model is installed.")
    print(error)
