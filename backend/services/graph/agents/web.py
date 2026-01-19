from ..tools import search_web_tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv
from rich import print
from rich.markdown import Markdown

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

web_agent = create_agent(
    model=llm,
    debug=False,
    system_prompt=load_prompt("web"),
    tools=[search_web_tool],
)

if __name__ == "__main__":
    user_input = "informações sobre a IBM políticas de contratação e serviços oferecidos?"
    response = web_agent.invoke({"messages": [user_input]})
    print(response)
    
    print(Markdown(response["messages"][-1].content))