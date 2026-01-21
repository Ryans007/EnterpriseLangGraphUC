from services.graph.graph import graph
from langgraph.graph.state import RunnableConfig
from langchain_core.messages import HumanMessage
import threading
from rich.markdown import Markdown
from rich import print

config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

def main():
    print("Bot Comparador de Tecnologia Iniciado!")
    print("Digite 'sair' para encerrar.\n")

    while True:
        msg = input("\nVocê: ")

        if msg.lower() in ['sair', 'exit', 'quit']:
            print("Até logo!")
            break

        if not msg.strip():
            continue

        # for s in graph.stream({
        #     'messages': [HumanMessage(content=msg)],
        # }, config=config):
        #     print(s)

        response = graph.invoke({'messages': [HumanMessage(content=msg)]}, config=config)
        
        print(Markdown(response['messages'][-1].content))
if __name__ == "__main__":
    main()
    
    


