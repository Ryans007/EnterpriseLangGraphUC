from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..utils import load_prompt
from pydantic import BaseModel
from rich import print
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

revisor_agent = create_agent(
    model=llm,
    debug=False,
    system_prompt=load_prompt("revisor"),
)
