from fastapi import APIRouter, Depends, HTTPException, Form
from config.database import get_db
from models import Message
from serializers import MessageSerializer, MessageRequest
from langchain_core.messages import HumanMessage
from langgraph.graph.state import RunnableConfig
from services.graph.graph import graph
from datetime import datetime
from pydantic import BaseModel
import uuid


router = APIRouter()

@router.post("/chat/", response_model=MessageSerializer)
def create_message(
    user_message: MessageRequest,
    db=Depends(get_db)
):
    """Rota para criar uma nova mensagem em um thread"""
    
    human_message = HumanMessage(content=user_message.user_message.strip())
    if user_message.thread_id is not None:
        thread_id = user_message.thread_id
    else:
        thread_id = str(uuid.uuid4())
        
    config = RunnableConfig(configurable={"thread_id": thread_id})

    response = graph.invoke({"messages": [human_message]}, config=config)
    ai_message = response["messages"][-1].content
    new_message = Message(
        thread_id=thread_id,
        user_message=human_message.content,
        ai_message=ai_message,
        create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return MessageSerializer(
        thread_id=new_message.thread_id,
        user_message=new_message.user_message,
        ai_message=new_message.ai_message,
        create_at=new_message.create_at
    )