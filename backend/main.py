import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="SiteForge Local Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5-coder"


class ProjectRequest(BaseModel):
  prompt: str


def call_ollama(system_prompt: str, user_prompt: str) -> dict:
  payload = {
      "model": MODEL_NAME,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_prompt},
      ],
      "stream": False,
      "format": "json",
  }
  try:
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    if response.status_code == 200:
      content = response.json()["message"]["content"]
      return json.loads(content)
    else:
      raise HTTPException(
          status_code=500, detail="Erro de comunicação com o Ollama local."
      )
  except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=(
            "Não foi possível conectar ao Ollama. Verifique se ele está aberto"
            f" no PC. Erro: {str(e)}"
        ),
    )


@app.post("/api/generate-site")
def generate_site(data: ProjectRequest):
  system_architect = (
      "Você é um Arquiteto Web Senior especializado em UX/UI. Analise o pedido"
      " do usuário e retorne um JSON estruturado contendo a lista de seções da"
      ' página (ex: hero, features, contact) e a paleta de cores. Chave principal'
      ' "plan".'
  )
  plan = call_ollama(system_architect, data.prompt)

  system_developer = (
      "Você é um Desenvolvedor Front-end expert em Tailwind CSS. Com base no"
      " plano fornecido, escreva um arquivo HTML único, moderno, responsivo e"
      " completo. Retorne um JSON contendo exclusivamente a chave 'html_code'"
      " com o código HTML em formato de texto."
  )
  code_result = call_ollama(system_developer, json.dumps(plan))

  return {
      "status": "success",
      "html": code_result.get(
          "html_code", "<h1>Erro ao gerar código HTML</h1>"
      ),
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="127.0.0.1", port=8000)
