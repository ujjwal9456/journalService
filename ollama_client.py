import json
import requests
from typing import List, Dict
import aiohttp

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:7b"

async def chat_stream(messages: List[Dict[str, str]]) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(OLLAMA_URL, json=payload) as response:
            async for line in response.content:
                if line:
                    yield json.loads(line.decode())
