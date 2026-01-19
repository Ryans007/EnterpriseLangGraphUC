from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from dotenv import load_dotenv
import os 

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

@tool
def search_web_tool(query: str) -> str:
    """
    Docstring for search_web_tool
    
    :param query: Texto da consulta de pesquisa na web
    :type query: str
    :return: Resultados da pesquisa na web
    :rtype: str
    """
    web_tool = TavilySearch(api_key=tavily_api_key, num_results=5)
    return web_tool.invoke({"query": query})