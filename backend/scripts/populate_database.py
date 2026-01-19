from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
from config.database import Base, engine
from models import SoftwareInventory, ComplianceStatus #

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    # Limpar tabela para evitar duplicatas 
    session.query(SoftwareInventory).delete()

    softwares = [
        SoftwareInventory(
            name="Anthropic Claude",
            category="GenAI/LLM",
            department="Engenharia",
            monthly_price=20.00,
            currency="USD",
            contract_start=date(2024, 1, 15),
            compliance_status=ComplianceStatus.APPROVED,
            data_residency="EUA (AWS)"
        ),
        
        SoftwareInventory(
            name="IBM",
            category="Plataforma de IA",
            department="Data Science",
            monthly_price=500.00,
            currency="USD",
            contract_start=date(2023, 11, 10),
            compliance_status=ComplianceStatus.APPROVED,
            data_residency="Híbrido (Brasil/EUA)"
        ),

        SoftwareInventory(
            name="Gaio",
            category="Data Analytics",
            department="BI & Analytics",
            monthly_price=1500.00,
            currency="BRL",
            contract_start=date(2024, 2, 1),
            compliance_status=ComplianceStatus.APPROVED,
            data_residency="Brasil"
        ),

        SoftwareInventory(
            name="Adobe Firefly (Video)",
            category="IA Vídeo",
            department="Marketing",
            monthly_price=150.00,
            currency="BRL",
            contract_start=date(2023, 6, 1),
            compliance_status=ComplianceStatus.APPROVED,
            data_residency="Europa"
        ),

        SoftwareInventory(
            name="ChatGPT Plus (Individual)",
            category="GenAI/LLM",
            department="Vendas",
            monthly_price=20.00,
            currency="USD",
            contract_start=date(2024, 5, 20),
            compliance_status=ComplianceStatus.PENDING,
            data_residency="EUA"
        )
    ]

    try:
        session.add_all(softwares)
        session.commit()
        print(f"\nBanco de dados povoado com {len(softwares)} softwares com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao povoar banco: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()