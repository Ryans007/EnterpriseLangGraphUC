from langgraph.graph.state import RunnableConfig
from langchain_core.messages import AIMessage

class Graph:
    def __init__(self):
        pass 
    def invoke(self, messages: dict, config: RunnableConfig) -> str:
        # Lógica para processar o prompt e gerar uma resposta
        return {"messages": [AIMessage(content="Olá, Tudo bem? Como posso ajudar você hoje?")]}
    
graph = Graph()