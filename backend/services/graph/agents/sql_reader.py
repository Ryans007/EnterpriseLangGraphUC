from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..tools import software_inventory_reader_tool, list_all_software_inventory_tool
from ..utils import load_prompt
from pydantic import BaseModel
from rich import print
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

sql_reader_agent = create_agent(
    model=llm,
    debug=False,
    system_prompt=load_prompt("sql_reader"),
    tools=[software_inventory_reader_tool, list_all_software_inventory_tool],
)

if __name__ == "__main__":
    # Exemplo de uso do orquestrador
    user_input = """Gostaria de saber se já possuímos alguma ferramenta similar ao ChatGPT em nosso inventário de software. Se sim, por favor, forneça os detalhes do contrato, como fornecedor, data de validade e número de usuários licenciados."""
    response = sql_reader_agent.invoke({"messages": [user_input]})
    print(response)
    
    print(Markdown(response["messages"][-1].content))