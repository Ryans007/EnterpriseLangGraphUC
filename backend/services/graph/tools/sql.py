from langchain_core.tools import tool
from sqlalchemy import select
from config.database import SessionLocal
from models import SoftwareInventory, ProcurementRequest

@tool
def software_inventory_reader_tool(query_type: str, search_term: str):
    """
    Consulta o inventário de software da empresa.
    Use esta tool para verificar se já possuímos ferramentas similares ou para saber detalhes de um contrato.
    
    Args:
        query_type: 'category' para buscar softwares similares ou 'name' para um software específico.
        search_term: O termo de busca (ex: 'IA Vídeo' ou 'Claude').
    """
    
    with SessionLocal() as session:
        if query_type == "category":
            stmt = select(SoftwareInventory).where(SoftwareInventory.category.ilike(f"%{search_term}%"))
        else:
            stmt = select(SoftwareInventory).where(SoftwareInventory.name.ilike(f"%{search_term}%"))
            
        results = session.execute(stmt).scalars().all()
        
        if not results:
            return "Nenhum software encontrado com esses critérios."
        
        return [
            {
                "nome": s.name, 
                "categoria": s.category, 
                "status": s.compliance_status.value,
                "onde_os_dados_ficam": s.data_residency
            } for s in results
        ]
        
@tool
def list_all_software_inventory_tool():
    """
    Retorna todo o inventário de software da empresa sem filtros.
    Use esta tool quando precisar de uma visão geral de todas as ferramentas.
    """
    with SessionLocal() as session:
        stmt = select(SoftwareInventory)
        results = session.execute(stmt).scalars().all()
        
        if not results:
            return "O inventário está vazio."
        
        return [
            {
                "nome": s.name, 
                "categoria": s.category, 
                "status": s.compliance_status.value,
                "onde_os_dados_ficam": s.data_residency
            } for s in results
        ]
        
@tool
def register_procurement_request(tool_name: str, category: str, risk_level: str, justification: str):
    """
    Registra uma nova solicitação de contratação de software no banco de dados para revisão do TI.
    Use esta tool somente após a análise do WebSearch e do RAG.
    
    Args:
        tool_name: Nome do software solicitado.
        category: Categoria do software.
        risk_level: Nível de risco identificado (Low, Medium, High).
        justification: Resumo do porquê a ferramenta está sendo solicitada e o parecer do RAG.
    """

    with SessionLocal() as session:
        new_request = ProcurementRequest(
            tool_name=tool_name,
            category=category,
            risk_level=risk_level,
            justification=justification
        )
        try:
            session.add(new_request)
            session.commit()
            return f"Sucesso: Solicitação para '{tool_name}' registrada com ID {new_request.id}."
        except Exception as e:
            session.rollback()
            return f"Erro ao registrar solicitação: {str(e)}"