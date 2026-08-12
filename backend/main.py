import os
import json
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

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"domain": "", "env_vars": "{}"}

class ProjectRequest(BaseModel):
    prompt: str

@app.get("/api/config")
async def get_config():
    return load_config()

@app.post("/api/config")
async def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return {"status": "success", "message": "Configurações salvas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gerar")
async def generate_app(request: ProjectRequest):
    try:
        project_path = os.path.join(WORKSPACE_DIR, "latest_project")
        os.makedirs(project_path, exist_ok=True)

        files_to_create = agent_architect(request.prompt)
        
        generated_files = []
        for file_name in files_to_create:
            file_code = agent_coder(request.prompt, file_name)
            file_code = file_code.replace(f"```{file_name.split('.')[-1]}", "").replace("```", "").strip()
            
            file_full_path = os.path.join(project_path, file_name)
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(file_code)
            generated_files.append(file_name)
                
        return {
            "status": "success",
            "files": generated_files,
            "preview_url": "/preview/index.html"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para servir o app gerado em tempo real
app.mount("/preview", StaticFiles(directory=os.path.join(WORKSPACE_DIR, "latest_project"), html=True), name="preview")
# Rota principal para o painel de controle
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
