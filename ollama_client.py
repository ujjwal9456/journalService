import requests
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:7b"

def chat(messages: List[Dict[str, str]]) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    
    result = response.json()
    return result["message"]["content"]
