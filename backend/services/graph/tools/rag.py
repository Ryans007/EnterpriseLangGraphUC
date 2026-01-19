from langchain_core.tools import tool 
from ..utils import VectorStore

@tool 
def retrieve_documents_tool(query: str, k: int = 5) -> str:
    """
    Ferramenta para recuperar documentos relevantes do vetor de documentos.

    :param query: Consulta de texto para buscar documentos relevantes
    :type query: str
    :param k: Número de documentos a recuperar, por padrão 5
    :type k: int, optional
    :return: Documentos recuperados como uma string concatenada
    :rtype: str
    """
    vectorstore = VectorStore.get_instance()
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "fetch_k": 20})
    docs = retriever.invoke(query)
    results = "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    
    return results if results else "Nenhum documento encontrado."