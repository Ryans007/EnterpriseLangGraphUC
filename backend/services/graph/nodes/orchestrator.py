from ..state import GraphState
from ..agents import orchestrator_agent

def orchestrator_node(state: GraphState) -> GraphState:
    print("> Nó Orquestrador acionado.")
    response = orchestrator_agent.invoke({
        "messages": [
            *state["messages"]
            ]
        })
    structured_response = response.get("structured_response")
    
    return  {
        "next_agent": structured_response.next_agent,
        "web_query": structured_response.web_query if structured_response.web_query else "",
        "flow": structured_response.flow,
        "orchestration_explanation": structured_response.explanation,
    }