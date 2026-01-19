from langgraph.graph.state import RunnableConfig
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import InMemorySaver
from .state import GraphState
from .nodes import (
    orchestrator_node,
    web_node,
    rag_node,
    revisor_node,
    sql_reader_node,
    sql_writer_node,
)


workflow = StateGraph(GraphState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("web", web_node)
workflow.add_node("rag", rag_node)
workflow.add_node("revisor", revisor_node)
workflow.add_node("sql_reader", sql_reader_node)
workflow.add_node("sql_writer", sql_writer_node)

workflow.add_edge(START, "orchestrator")

workflow.add_conditional_edges(
    "orchestrator",
    lambda state: state["next_agent"],
    {
        "WebAgent": "web", 
        "RagAgent": "rag", 
        "SqlAgent": "sql_reader"
    },
)

workflow.add_conditional_edges(
    "web",
    lambda state: state["flow"],
    {
        "Complete": "rag",
        "Partial": "revisor"
    },
)

workflow.add_conditional_edges(
    "rag",
    lambda state: state["flow"],
    {
        "Complete": "sql_reader",
        "Partial": "revisor"
    },
)

workflow.add_conditional_edges(
    "sql_reader",
    lambda state: state["flow"],
    {
        "Complete": "sql_writer",
        "Partial": "revisor"
    },
)

workflow.add_edge("sql_writer", "revisor")
workflow.add_edge("revisor", END)

memory = InMemorySaver()

graph = workflow.compile(checkpointer=memory)