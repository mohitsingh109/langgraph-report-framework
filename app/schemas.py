from pydantic import BaseModel, Field
from typing import Dict, Any


class ChatRequest(BaseModel):
    conversation_id: str = Field(default="1")
    message: str = Field(..., min_length=1)

# AI Response
class ChatResponse(BaseModel):
    conversation_id: str
   # status: str
    reply: str
   # data: Dict[str, Any] = {}
