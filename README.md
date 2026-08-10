# SiteForge Local 🚀

O **SiteForge Local** é uma IDE de desktop minimalista e focada em privacidade que utiliza múltiplos agentes de IA locais (via **Ollama**) para planejar e criar Landing Pages e mini-sites profissionais em segundos, sem mensalidades e sem depender da nuvem.

---

## ✨ Principais Recursos

* **100% Offline e Privado:** Seus dados e códigos nunca saem do seu computador.
* **Preço Único (Lifetime):** Pague uma vez e tenha a ferramenta para sempre, sem custos recorrentes de APIs de IA de terceiros.
* **Arquitetura de Múltiplos Agentes:** Conta com um *Agente Arquiteto* (responsável pelo planejamento de UX/UI) e um *Agente Desenvolvedor* (geração de código limpo com HTML e Tailwind CSS).
* **Pré-visualização em Tempo Real:** Veja o site gerado instantaneamente na tela ao lado do chat.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python + FastAPI (gerenciamento dos agentes locais)
* **Frontend:** React + Tailwind CSS (interface moderna e fluida)
* **Motor de IA:** Ollama (rodando modelos open-source como o `qwen2.5-coder`)

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter instalado no seu computador:
1. [Python](https://www.python.org/) (versão 3.10 ou superior)
2. [Node.js](https://nodejs.org/)
3. [Ollama](https://ollama.com/) instalado e com o modelo de código baixado:
   ```bash
   ollama run qwen2.5-coder

