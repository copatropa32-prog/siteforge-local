from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Configuração de CORS para o React conseguir falar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_site(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "")
    
    # Aqui vamos integrar com o Ollama localmente
    # Por enquanto, ele retorna o que recebeu para testarmos a conexão
    return {
        "status": "success",
        "message": f"IA recebendo: {user_prompt}",
        "code": "<!-- Seu código gerado aparecerá aqui -->"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

