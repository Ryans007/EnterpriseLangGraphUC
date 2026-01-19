from typing import TypedDict, Literal
from pydantic import BaseModel


class OrchestratorOutputSchema(BaseModel):
    """Esquema de saída para o orquestrador de mensagens"""

    explanation: str 
    web_query: str | None = None
    next_agent: Literal["WebAgent", "RagAgent", "SqlAgent"]
    flow: Literal["Complete", "Partial"]