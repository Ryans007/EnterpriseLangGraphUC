from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import Optional
from pathlib import Path 
from dotenv import load_dotenv
import os

load_dotenv()


class VectorStore: 
    """Padrão Singleton para gerenciar a instância do vetor de documentos."""
    __instance: Optional[FAISS] = None
    __PATH = Path(__file__).resolve().parent.parent.parent.parent
    __INDEX_PATH = "config/faiss_index" 
    
    @classmethod
    def get_instance(cls) -> FAISS:
        if cls.__instance is not None:
            print("Retornando instância da memória RAM.")
            return cls.__instance    
                
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        if os.path.exists(cls.__INDEX_PATH):
            print("Índice encontrado no disco. Carregando...")
            cls.__instance = FAISS.load_local(
                cls.__INDEX_PATH, 
                embeddings, 
                allow_dangerous_deserialization=True 
            )
        else:
            print("Índice não encontrado. Processando PDF...")
            loader = PyPDFLoader(str(cls.__PATH / "docs/politicas_internas.pdf"))
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            splits = text_splitter.split_documents(documents)

            cls.__instance = FAISS.from_documents(documents=splits, embedding=embeddings)
            
            cls.__instance.save_local("config/faiss_index")
            print("Vetor store criado e salvo no disco.")
        return cls.__instance

if __name__ == "__main__":
    VectorStore.get_instance()
    print("VectorStore instanciado com sucesso.")
