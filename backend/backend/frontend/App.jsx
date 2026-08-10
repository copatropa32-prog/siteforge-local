import React, { useState } from 'react';

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [htmlCode, setHtmlCode] = useState('<div class="flex items-center justify-center h-screen bg-gray-100 text-gray-500"><p>Digite algo ao lado para os agentes criarem seu site!</p></div>');

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/generate-site', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      if (data.html) {
        setHtmlCode(data.html);
      }
    } catch (err) {
      alert('Erro ao conectar com o backend local. O Ollama e o Python estão rodando?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans">
      {/* Painel Esquerdo: Chat com Agentes */}
      <div className="w-1/3 flex flex-col border-r border-gray-800 p-4">
        <h1 className="text-xl font-bold mb-4 text-indigo-400">SiteForge Local 🚀</h1>
        <p className="text-sm text-gray-400 mb-4">Descreva o site que você quer criar. Os agentes locais farão o trabalho.</p>
        
        <textarea
          className="flex-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm resize-none focus:outline-none focus:border-indigo-500 mb-4"
          placeholder="Ex: Landing page para uma barbearia moderna com botão de WhatsApp..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50"
        >
          {loading ? 'Agentes trabalhando...' : 'Criar Site com IA'}
        </button>
      </div>

      {/* Painel Direito: Preview ao Vivo do Site */}
      <div className="w-2/3 bg-white flex flex-col">
        <div className="bg-gray-800 text-xs text-gray-400 px-4 py-2 border-b border-gray-700 flex justify-between items-center">
          <span>Pré-visualização ao Vivo</span>
          <span className="text-green-400">● Localhost Ativo</span>
        </div>
        <iframe
          title="Preview"
          className="w-full flex-1 border-none"
          srcDoc={htmlCode}
        />
      </div>
    </div>
  );
}
