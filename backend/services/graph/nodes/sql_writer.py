from ..state import GraphState
from ..agents import sql_writer_agent

def sql_writer_node(state: GraphState) -> GraphState:
    print("> Nó SQL Writer acionado.")
    response = sql_writer_agent.invoke({
        "messages": [
            *state["messages"]
            ]
        })
    
    return {
        "messages": [response["messages"][-1]],
    }