import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents import agent_architect, agent_coder # Importa o que criamos no agents.py

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para a pasta onde ficam os arquivos do site (frontend)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

class ProjectRequest(BaseModel):
    prompt: str

@app.post("/api/gerar")
async def generate_app(request: ProjectRequest):
    try:
        # Aqui entra a lógica dos agentes
        files_to_create = agent_architect(request.prompt)
        
        # Gera os arquivos dentro da pasta frontend
        for file_name in files_to_create:
            file_code = agent_coder(request.prompt, file_name)
            file_code = file_code.replace("```html", "").replace("```", "").strip()
            
            with open(os.path.join(FRONTEND_DIR, file_name), "w", encoding="utf-8") as f:
                f.write(file_code)
                
        return {"status": "success", "files": files_to_create}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir o frontend (index.html e outros) na raiz
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
