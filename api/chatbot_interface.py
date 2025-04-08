# api/chatbot_interface.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_llama(request: ChatRequest):
    # Simulated response for now — we'll connect it to LLaMA next
    user_message = request.message
    response = f"🤖 LLaMA says: I received your message: '{user_message}'"
    return {"response": response}
