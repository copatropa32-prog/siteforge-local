import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Inicialização do App
app = FastAPI(title="SiteForge Local Agent")

# Configuração de CORS (Essencial para o React falar com o Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Ollama
OLLAMA_URL = "http://localhost:11434/api"
MODEL_NAME = "qwen2.5-coder"

# Modelo de dados para validar o que vem do frontend
class ProjectRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_site(request: ProjectRequest):
    try:
        # Envia o pedido para o Ollama local
        response = requests.post(
            f"{OLLAMA_URL}/generate",
            json={
                "model": MODEL_NAME,
                "prompt": f"Write a complete HTML landing page code based on this description: {request.prompt}. Return ONLY the code.",
                "stream": False
            }
        )
        
        # Verifica se o Ollama respondeu com sucesso
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from Ollama")
            
        return response.json()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


