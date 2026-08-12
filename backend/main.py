import os
import json
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents import agent_architect, agent_coder, agent_debugger, agent_modifier

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

current_status_log = "Sistema pronto e aguardando comando..."

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"domain": "", "env_vars": "{}", "model": "llama3"}

class ProjectRequest(BaseModel):
    prompt: str

class FileSaveRequest(BaseModel):
    path: str
    content: str

class FileActionRequest(BaseModel):
    path: str

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

@app.get("/api/status")
async def get_status():
    return {"status": current_status_log}

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

@app.post("/api/file-content")
async def save_file_content(request: FileSaveRequest):
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    file_full_path = os.path.join(project_path, request.path)
    if not os.path.exists(file_full_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    try:
        with open(file_full_path, "w", encoding="utf-8") as f:
            f.write(request.content)
        return {"status": "success", "message": "Arquivo salvo com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/file-create")
async def create_file(request: FileActionRequest):
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    file_full_path = os.path.join(project_path, request.path)
    if os.path.exists(file_full_path):
        raise HTTPException(status_code=400, detail="Arquivo já existe")
    try:
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        with open(file_full_path, "w", encoding="utf-8") as f:
            f.write("<!-- Novo arquivo criado manualmente -->\n")
        return {"status": "success", "message": "Arquivo criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/file-delete")
async def delete_file(request: FileActionRequest):
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    file_full_path = os.path.join(project_path, request.path)
    if not os.path.exists(file_full_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    try:
        os.remove(file_full_path)
        return {"status": "success", "message": "Arquivo excluído com sucesso!"}
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
    global current_status_log
    config = load_config()
    model_name = config.get("model", "llama3")
    
    try:
        project_path = os.path.join(WORKSPACE_DIR, "latest_project")
        os.makedirs(project_path, exist_ok=True)

        current_status_log = f"🤖 [Modelo: {model_name}] Arquiteto planejando estrutura..."
        files_to_create = agent_architect(request.prompt, model_name)
        current_status_log = f"📁 Estrutura planejada: {files_to_create}"

        generated_files = []
        for file_name in files_to_create:
            current_status_log = f"💻 Coder escrevendo o código para: {file_name}..."
            file_code = agent_coder(request.prompt, file_name, model_name)
            file_code = file_code.replace(f"```{file_name.split('.')[-1]}", "").replace("```", "").strip()
            
            current_status_log = f"🛠️ Debugger revisando o código de: {file_name}..."
            fixed_code = agent_debugger(file_code, file_name, model_name)
            fixed_code = fixed_code.replace(f"```{file_name.split('.')[-1]}", "").replace("```", "").strip()
            
            file_full_path = os.path.join(project_path, file_name)
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)
            generated_files.append(file_name)
                
        current_status_log = "✅ Projeto gerado e revisado com sucesso!"
        return {
            "status": "success",
            "files": generated_files,
            "preview_url": "/preview/index.html"
        }
    except Exception as e:
        current_status_log = f"❌ Erro durante o processo: {str(e)}"
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/modificar")
async def modify_app(request: ProjectRequest):
    global current_status_log
    config = load_config()
    model_name = config.get("model", "llama3")
    
    project_path = os.path.join(WORKSPACE_DIR, "latest_project")
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Nenhum projeto encontrado para modificar")
    
    try:
        current_status_log = f"🤖 [Modelo: {model_name}] Agente Modificador analisando pedido..."
        
        files_content = {}
        for root, _, filenames in os.walk(project_path):
            for name in filenames:
                rel_path = os.path.relpath(os.path.join(root, name), project_path)
                with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                    files_content[rel_path] = f.read()
                    
        files_str = json.dumps(files_content, ensure_ascii=False, indent=2)
        
        current_status_log = "💻 Aplicando modificações cirúrgicas nos arquivos..."
        modifications = agent_modifier(files_str, request.prompt, model_name)
        
        modified_files = []
        for file_name, new_code in modifications.items():
            clean_code = new_code.replace(f"```{file_name.split('.')[-1]}", "").replace
