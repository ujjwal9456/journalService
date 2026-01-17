import json
import os
from datetime import datetime
from typing import List, Dict

DATA_DIR = "data"

def get_today_filename() -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_DIR, f"{today}.jsonl")

def save_message(role: str, content: str) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    
    message = {
        "ts": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    
    filename = get_today_filename()
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(message) + "\n")

def load_conversation() -> List[Dict[str, str]]:
    filename = get_today_filename()
    
    if not os.path.exists(filename):
        return []
    
    messages = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                message = json.loads(line)
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
    
    return messages
