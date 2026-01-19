from services.graph.graph import graph
from langgraph.graph.state import RunnableConfig
from langchain_core.messages import HumanMessage
import threading
from rich.markdown import Markdown
from rich import print

config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

def test_graph_invocation():
    """Teste de invocação do grafo de estados"""
    human_message = HumanMessage(content="Detalhe o Claude")
    
    # for s in graph.stream({
    # 'messages': [human_message],
    # }, config=config):
    #     print(s)
    
    response = graph.invoke({"messages": [human_message]}, config=config)
    
    print(Markdown(response['messages'][-1].content))
    print(Markdown("---"))
    print("Estado do grafo após invocação:")
    print(graph.get_state(config=config))

if __name__ == "__main__":
    test_graph_invocation()
    
    


