import json
import requests
from typing import List, Dict, AsyncGenerator
import aiohttp


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:7b"
TIMEOUT = aiohttp.ClientTimeout(total=300, connect=10)

async def chat_stream(messages: List[Dict[str, str]]) -> AsyncGenerator[Dict, None]:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }
    
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.post(OLLAMA_URL, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Error: {response.status} - {error_text}")
            async for line in response.content:
                if line:
                    try:
                        yield json.loads(line.decode())
                    except json.JSONDecodeError:
                        continue
