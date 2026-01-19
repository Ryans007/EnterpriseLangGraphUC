from typing import TypedDict, Literal, Sequence, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """Estado do grafo de mensagens"""

    orchestration_explanation: str
    web_query: str
    web_results: str
    next_agent: str
    flow: Literal["Complete", "Partial"]
    messages: Annotated[Sequence[BaseMessage], add_messages]