import os
import json
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents import agent_architect, agent_coder, agent_debugger

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

@app.get("/api/files")
async def list_project_files():
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    if not os.path.exists(project_path):
        return []
    files = []
    for root, _, filenames in os.walk(project_path):
        for name in filenames:
            rel_path = os.path.relpath(os.path.join(root, name), project_path)
            files.append(rel_path)
    return files

@app.get("/api/file-content")
async def get_file_content(path: str):
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    file_full_path = os.path.join(project_path, path)
    if not os.path.exists(file_full_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    try:
        with open(file_full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download")
async def download_project():
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Nenhum projeto encontrado para download")
    
    zip_base_path = os.path.join(WORKSPACE_DIR, "projeto_exportado")
    shutil.make_archive(zip_base_path, 'zip', project_path)
    return FileResponse(f"{zip_base_path}.zip", media_type="application/zip", filename="siteforge_projeto.zip")

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
            
            fixed_code = agent_debugger(file_code, file_name)
            fixed_code = fixed_code.replace(f"```{file_name.split('.')[-1]}", "").replace("```", "").strip()
            
            file_full_path = os.path.join(project_path, file_name)
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)
            generated_files.append(file_name)
                
        return {
            "status": "success",
            "files": generated_files,
            "preview_url": "/preview/index.html"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/preview", StaticFiles(directory=os.path.join(WORKSPACE_DIR, "latest_project"), html=True), name="preview")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
