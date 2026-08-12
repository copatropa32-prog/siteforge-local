import os
import json
import shutil
import subprocess
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Configuração de Pastas
WORKSPACE = "workspace"
CONFIG_FILE = "config.json"
if not os.path.exists(WORKSPACE):
    os.makedirs(WORKSPACE)

# Modelos de Dados
class FileAction(BaseModel):
    path: str
    content: str = None

class TerminalInput(BaseModel):
    input: str

class PromptAction(BaseModel):
    prompt: str

# --- Servir arquivos estáticos ---
# Monta a pasta raiz como estática para o frontend e o workspace para preview
app.mount("/preview", StaticFiles(directory=WORKSPACE), name="workspace")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# --- API de Arquivos ---
@app.get("/api/files")
async def list_files():
    files = [f for f in os.listdir(WORKSPACE) if os.path.isfile(os.path.join(WORKSPACE, f))]
    return files

@app.get("/api/file-content")
async def get_file_content(path: str):
    file_path = os.path.join(WORKSPACE, path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}

@app.post("/api/file-content")
async def save_file(action: FileAction):
    file_path = os.path.join(WORKSPACE, action.path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(action.content)
    return {"status": "success"}

@app.post("/api/file-create")
async def create_file(action: FileAction):
    file_path = os.path.join(WORKSPACE, action.path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("")
    return {"status": "success"}

@app.post("/api/file-delete")
async def delete_file(action: FileAction):
    file_path = os.path.join(WORKSPACE, action.path)
    if os.path.exists(file_path):
        os.remove(file_path)
    return {"status": "success"}

# --- API de Terminal e Agentes ---
@app.post("/api/terminal-input")
async def handle_terminal(data: TerminalInput):
    # ATENÇÃO: Executa comandos no shell. Mantenha rodando apenas localmente.
    cmd = data.input.strip()
    if not cmd: return {"status": "empty"}
    
    try:
        # Executa o comando no diretório do workspace
        result = subprocess.run(cmd, shell=True, cwd=WORKSPACE, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return {"output": output}
    except Exception as e:
        return {"output": str(e)}

@app.post("/api/gerar")
async def gerar_projeto(action: PromptAction):
    # Aqui você integra sua lógica de IA (LLM/Agent)
    print(f"Gerando projeto com prompt: {action.prompt}")
    return {"status": "Gerando..."}

@app.post("/api/modificar")
async def modificar_projeto(action: PromptAction):
    print(f"Modificando projeto: {action.prompt}")
    return {"status": "Modificando..."}

# --- Configurações ---
@app.get("/api/config")
async def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"model": "llama3"}

@app.post("/api/config")
async def save_config(data: dict):
    with open(CONFIG_FILE, "w") as f: json.dump(data, f)
    return {"status": "success"}

@app.get("/api/download")
async def download_project():
    shutil.make_archive("projeto", 'zip', WORKSPACE)
    return FileResponse("projeto.zip", media_type='application/zip', filename="projeto.zip")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
