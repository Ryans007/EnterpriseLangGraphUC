from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..tools import retrieve_documents_tool
from ..utils import load_prompt
from pydantic import BaseModel
from rich import print
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

rag_agent = create_agent(
    model=llm,
    debug=False,
    system_prompt=load_prompt("rag"),
    tools=[retrieve_documents_tool],
)

if __name__ == "__main__":
    # Exemplo de uso do orquestrador
    user_input = """### Visão Geral\nA IBM oferece uma ampla gama de serviços, incluindo soluções em nuvem, software, consultoria e suporte técnico. A empresa é reconhecida por sua       
inovação em tecnologia e serviços de TI.\n\n### Soberania de Dados\n- **Local de Armazenamento e Processamento:** Informação não localizada publicamente.\n\n### Privacidade e IA\n- **Uso  
de Dados para Treinamento:** A IBM não utiliza informações pessoais processadas sob contrato para fins de marketing e publicidade sem consentimento expresso. No entanto, a política não    
menciona explicitamente o uso de dados para treinar modelos de IA.\n\n### Segurança Técnica\n- **Padrões de Criptografia:** Informação não localizada publicamente. A IBM menciona a        
proteção de dados, mas não especifica os padrões de criptografia utilizados em seus serviços.\n\n### Redundância\n- **Concorrentes Principais:**\n  1. Microsoft Azure\n  2. Amazon Web     
Services (AWS)\n  3. Google Cloud Platform\n\n### Fontes\n- [IBM Privacy Statement](https://www.ibm.com/us-en/privacy)\n- [IBM Terms of Use](https://www.ibm.com/legal/terms)\n- [IBM Cloud 
Terms of Use](https://cloud.ibm.com/docs/overview?topic=overview-terms)"""
    response = rag_agent.invoke({"messages": [user_input]})
    print(response)
    
    print(Markdown(response["messages"][-1].content))