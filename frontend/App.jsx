import { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    setIsGenerating(true);
    // Aqui entra a lógica de comunicação com seu backend no futuro
    console.log("Gerando site para:", prompt);
    setTimeout(() => setIsGenerating(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6 flex flex-col items-center justify-center text-white">
      <div className="w-full max-w-2xl bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <h1 className="text-3xl font-bold mb-6 text-indigo-400">SiteForge Local</h1>
        
        <textarea
          className="w-full h-32 bg-slate-950 border border-slate-700 rounded-lg p-4 mb-4 focus:outline-none focus:border-indigo-500 transition"
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
      </div>
    </div>
  );
}

export default App;

