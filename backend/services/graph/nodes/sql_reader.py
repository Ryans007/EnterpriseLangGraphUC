from ..state import GraphState
from ..agents import sql_reader_agent

def sql_reader_node(state: GraphState) -> GraphState:
    print("> Nó SQL Reader acionado.")
    response = sql_reader_agent.invoke({
        "messages": [
            *state["messages"]
            ]
        })
    
    return {
        "messages": [response["messages"][-1]],
    }