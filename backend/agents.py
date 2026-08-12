import json
import requests

OLLAMA_URL = "http://localhost:11434/api"

def call_ollama(prompt, system_instruction="", model_name="llama3"):
    full_prompt = f"{system_instruction}\n\nUser Request: {prompt}" if system_instruction else prompt
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/generate", json=payload, timeout=300)
        if response.status_code == 200:
            return response.json().get("response", "")
        raise Exception(f"Erro no Ollama: {response.status_code}")
    except Exception as e:
        raise Exception(f"Falha na comunicação com a IA: {str(e)}")

def agent_architect(user_prompt, model_name="llama3"):
    system = (
        "You are a Software Architect AI. Given a user request, return a JSON array "
        "containing the list of files to create for a complete web application. "
        "Example format: [\"index.html\", \"styles.css\", \"app.js\"]. "
        "Return ONLY valid JSON array. No markdown code blocks."
    )
    response = call_ollama(user_prompt, system, model_name)
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != 0:
            return json.loads(response[start:end])
        return ["index.html"]
    except Exception:
        return ["index.html"]

def agent_coder(user_prompt, file_name, model_name="llama3"):
    system = (
        f"You are an expert Fullstack Developer. Write the complete, production-ready "
        f"code for the file: {file_name}, based on the user request. Use modern "
        f"frameworks via CDN (Tailwind CSS, Alpine.js, etc.) if web-based. Return "
        f"ONLY the raw code inside the file. No explanations, no markdown blocks."
    )
    return call_ollama(user_prompt, system, model_name)

def agent_debugger(file_code, file_name, model_name="llama3"):
    system = (
        f"You are a Senior Code Reviewer and Debugger. Review the following code for "
        f"the file '{file_name}'. Fix any syntax errors, unclosed tags, or broken references. "
        f"Return ONLY the corrected, raw code. No explanations, no markdown blocks."
    )
    return call_ollama(file_code, system, model_name)

def agent_modifier(project_files_str, user_prompt, model_name="llama3"):
    system = (
        "You are an expert Fullstack Developer Modifier AI. Given the existing project files content "
        "and a user modification request, return a JSON object where keys are the filenames to update "
        "and values are the complete updated code for those files. "
        "Return ONLY valid JSON. No markdown code blocks."
    )
    full_prompt = f"Existing Files:\n{project_files_str}\n\nModification Request: {user_prompt}"
    response = call_ollama(full_prompt, system, model_name)
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(response[start:end])
        return {}
    except Exception:
        return {}
