from ..state import GraphState
from ..agents import web_agent
from langchain_core.messages import HumanMessage

def web_node(state: GraphState) -> GraphState:
    print("> Nó Web acionado.")
    response = web_agent.invoke(
        {
            "messages": HumanMessage(state["web_query"])}
        )
    
    return {
        "messages": [response["messages"][-1]],
    }