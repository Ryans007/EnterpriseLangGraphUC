from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from config.database import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Evento de inicialização do aplicativo FastAPI"""
    try: 
        print("Iniciando o banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Banco de dados iniciado com sucesso!")
    except Exception as e:
        print(f"Erro ao iniciar o banco de dados: {e}")
        
app.include_router(chat_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
