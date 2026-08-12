import os
import shutil
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents import agent_architect, agent_coder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

class ProjectRequest(BaseModel):
    prompt: str

@app.post("/generate-app")
async def generate_app(request: ProjectRequest):
    try:
        project_id = str(uuid.uuid4())[:8]
        project_path = os.path.join(WORKSPACE_DIR, project_id)
        os.makedirs(project_path, exist_ok=True)

        # Passo 1: O Agente Arquiteto define os arquivos
        files_to_create = agent_architect(request.prompt)

        generated_files = []
        # Passo 2: O Agente Coder cria o conteúdo de cada arquivo
        for file_name in files_to_create:
            file_code = agent_coder(request.prompt, file_name)
            
            # Limpeza de marcações extras de markdown
            file_code = file_code.replace(f"```{file_name.split('.')[-1]}", "").replace("```", "").strip()

            file_full_path = os.path.join(project_path, file_name)
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(file_code)
            generated_files.append(file_name)

        return {
            "status": "success",
            "project_id": project_id,
            "files": generated_files,
            "preview_url": f"/preview/{project_id}/index.html"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para visualizar as aplicações geradas pelos agentes em tempo real
app.mount("/preview", StaticFiles(directory=WORKSPACE_DIR, html=True), name="preview")
