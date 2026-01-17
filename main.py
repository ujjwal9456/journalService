from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

from ollama_client import chat
from storage import save_message, load_conversation
from prompts import COMPANION_PROMPT

app = FastAPI(title="Journal CLI Middleware")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert Pydantic models to dict format for ollama_client
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Save user message
        if messages and messages[-1]["role"] == "user":
            save_message("user", messages[-1]["content"])
        
        # Get conversation history and add system prompt
        conversation_history = load_conversation()
        if not conversation_history:
            conversation_history.insert(0, {"role": "system", "content": COMPANION_PROMPT})
        
        # Get response from Ollama
        response = chat(conversation_history)
        
        # Save assistant response
        save_message("assistant", response)
        
        return ChatResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Journal CLI Middleware Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
