from ..state import GraphState
from ..agents import rag_agent

def rag_node(state: GraphState) -> GraphState:
    print("> Nó RAG acionado.")
    response = rag_agent.invoke({
        "messages": [
            *state["messages"]
            ]
        })
    
    return {
        "messages": [response["messages"][-1]],
    }