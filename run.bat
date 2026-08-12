@echo off
cls
echo ===================================================
echo       INICIANDO O SITEFORGE LOCAL (MULTI-AGENTES)
echo ===================================================

echo [1/3] Verificando e instalando dependencias do Python...
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [2/3] Iniciando o servidor FastAPI...
start cmd /k "uvicorn main:app --reload --port 8000"

echo [3/3] Abrindo o painel no navegador...
timeout /t 3 >nul
start http://localhost:8000

echo ===================================================
echo Tudo pronto! O servidor esta rodando na porta 8000.
echo ===================================================
pause
