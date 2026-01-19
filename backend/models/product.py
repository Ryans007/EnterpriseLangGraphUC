from sqlalchemy import Column, Integer, String, Float, Date, Enum, Text
from config.database import Base 
from datetime import date
import enum

class ComplianceStatus(enum.Enum):
    APPROVED = "Aprovado"
    PENDING = "Em Revisão"
    REJECTED = "Reprovado"
    DEPRECATED = "Descontinuado"

class SoftwareInventory(Base):
    __tablename__ = "software_inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)  # Ex: 'IA Vídeo', 'Design', 'Cloud'
    department = Column(String(50), nullable=False) # Ex: 'Marketing', 'TI', 'RH'
    
    # Dados Financeiros e Contratuais
    monthly_price = Column(Float, nullable=False)
    currency = Column(String(3), default="BRL")    # BRL, USD, EUR
    contract_start = Column(Date, nullable=False)
    contract_end = Column(Date, nullable=True)     # Null se for assinatura recorrente
    
    # Governança e LGPD
    compliance_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    data_residency = Column(String(50))             # Ex: 'Brasil', 'EUA', 'Europa'

class ProcurementRequest(Base):
    __tablename__ = "procurement_requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_name = Column(String(100), nullable=False)
    category = Column(String(50))
    justification = Column(Text)
    risk_level = Column(String(20)) # Low, Medium, High
    status = Column(String(20), default="Aguardando Revisão Humana")
    request_date = Column(Date, default=date.today)