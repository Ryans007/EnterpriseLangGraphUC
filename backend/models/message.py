from sqlalchemy import Column, Integer, String, DateTime

from pydantic import BaseModel 
from config.database import Base 


class Message(Base):
    """Classe que representa uma mensagem trocada em um thread no banco de dados"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String, nullable=True)
    create_at = Column(String, nullable=False)