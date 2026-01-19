from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..schemas import OrchestratorOutputSchema
from ..utils import load_prompt
from pydantic import BaseModel
from rich import print
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

orchestrator_agent = create_agent(
    model=llm,
    debug=False,
    system_prompt=load_prompt("orchestrator"),
    response_format=ProviderStrategy(OrchestratorOutputSchema)
)

if __name__ == "__main__":
    # Exemplo de uso do orquestrador
    user_input = "A equipe de IA está querendo contratar a IBM, queria verificar a viabilidade dessa contratação."
    response = orchestrator_agent.invoke({"messages": [user_input]})
    print(response.get("structured_response"))