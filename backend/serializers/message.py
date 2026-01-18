from typing import Optional
from pydantic import BaseModel


class MessageRequest(BaseModel):
    """Serializer para requisições de mensagens"""

    thread_id: str | None  = None
    user_message: str
    
    
class MessageSerializer(BaseModel):
    """Serializer para a classe Message"""

    thread_id: str
    user_message: str
    ai_message: Optional[str] = None
    create_at: str