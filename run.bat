@echo off
echo Iniciando o SiteForge Local...

:: Abre o Backend em uma nova janela
start cmd /k "echo Iniciando Backend... && cd backend && python main.py"

:: Abre o Frontend em outra nova janela
start cmd /k "echo Iniciando Frontend... && cd frontend && npm run dev"

echo Ambos os servidores foram iniciados.
echo Pressione qualquer tecla para fechar este script.
pause
