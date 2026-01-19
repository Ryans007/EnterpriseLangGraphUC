from ..state import GraphState
from ..agents import revisor_agent

def revisor_node(state: GraphState) -> GraphState:
    print("> Nó Revisor acionado.")
    response = revisor_agent.invoke({
        "messages": [
            *state["messages"]
            ]
        })
    
    return {
        "messages": [response["messages"][-1]],
    }