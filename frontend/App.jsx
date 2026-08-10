import { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [resultCode, setResultCode] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setIsGenerating(true);
    setResultCode('');

    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      if (response.ok) {
        // Exibe o código ou a resposta que veio do Ollama via Python
        setResultCode(data.response || JSON.stringify(data, null, 2));
      } else {
        setResultCode('Erro ao gerar o código no servidor.');
      }
    } catch (error) {
      console.error('Erro de conexão:', error);
      setResultCode('Erro: Não foi possível conectar ao backend Python.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6 flex flex-col items-center justify-center text-white">
      <div className="w-full max-w-2xl bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <h1 className="text-3xl font-bold mb-6 text-indigo-400">SiteForge Local</h1>
        
        <textarea
          className="w-full h-32 bg-slate-950 border border-slate-700 rounded-lg p-4 mb-4 focus:outline-none focus:border-indigo-500 transition text-sm"
          placeholder="Descreva o site que você quer criar..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className={`w-full py-3 rounded-lg font-bold transition ${
            isGenerating 
              ? 'bg-slate-700 cursor-not-allowed' 
              : 'bg-indigo-600 hover:bg-indigo-500'
          }`}
        >
          {isGenerating ? 'IA trabalhando...' : 'Gerar Código'}
        </button>

        {resultCode && (
          <div className="mt-6">
            <h3 className="text-sm font-semibold text-slate-400 mb-2">Código Gerado:</h3>
            <pre className="w-full h-40 bg-slate-950 border border-slate-800 rounded-lg p-4 overflow-auto text-xs text-green-400 font-mono">
              {resultCode}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;


