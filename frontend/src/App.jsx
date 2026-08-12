import React, { useState } from 'react';

export default function App() {
  // Estados para controlar a aba ativa no celular e a gaveta de arquivos
  const [activeTab, setActiveTab] = useState('editor'); // 'files' | 'editor' | 'prompt'
  const [isFilesOpen, setIsFilesOpen] = useState(false);
  const [promptText, setPromptText] = useState('');

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      
      {/* Topo: Cabeçalho Compacto */}
      <header className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b border-slate-800 z-10">
        <div className="flex items-center gap-2">
          <button 
            onClick={() => setIsFilesOpen(!isFilesOpen)}
            className="text-slate-400 hover:text-white p-1"
          >
            📁
          </button>
          <h1 className="text-sm font-bold tracking-wide">SiteForge IDE</h1>
        </div>
        <button className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded-md font-medium transition">
          Salvar
        </button>
      </header>

      {/* Corpo Principal (Alterna conforme a aba ativa) */}
      <main className="flex-1 relative overflow-hidden flex">
        
        {/* Gaveta Lateral de Arquivos (Drawer) */}
        {isFilesOpen && (
          <div className="absolute inset-y-0 left-0 w-3/4 max-w-xs bg-slate-900 border-r border-slate-800 z-30 p-4 flex flex-col shadow-2xl transition-transform">
            <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Arquivos</span>
              <button onClick={() => setIsFilesOpen(false)} className="text-slate-400 hover:text-white text-sm">✕</button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-1 text-sm text-slate-300">
              <div className="p-2 hover:bg-slate-800 rounded cursor-pointer">index.html</div>
              <div className="p-2 hover:bg-slate-800 rounded cursor-pointer">style.css</div>
              <div className="p-2 hover:bg-slate-800 rounded cursor-pointer">script.js</div>
            </div>
          </div>
        )}

        {/* Overlay para fechar a gaveta ao tocar fora */}
        {isFilesOpen && (
          <div 
            onClick={() => setIsFilesOpen(false)} 
            className="absolute inset-0 bg-black/50 z-20 backdrop-blur-xs"
          />
        )}

        {/* Conteúdo Dinâmico Central */}
        <div className="flex-1 flex flex-col h-full bg-slate-950">
          {activeTab === 'files' && (
            <div className="p-4 overflow-y-auto h-full">
              <h2 className="text-sm font-bold mb-3 text-slate-400">Gerenciador de Arquivos</h2>
              <div className="space-y-2 text-sm">
                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">index.html</div>
                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">style.css</div>
                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">script.js</div>
              </div>
            </div>
          )}

          {activeTab === 'editor' && (
            <div className="flex-1 flex flex-col h-full bg-[#1e1e1e]">
              <div className="bg-[#2d2d2d] px-4 py-2 text-xs text-slate-400 border-b border-slate-800 flex items-center justify-between">
                <span>index.html</span>
                <span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded">HTML</span>
              </div>
              <textarea 
                className="flex-1 bg-transparent p-4 text-sm font-mono text-slate-200 resize-none focus:outline-none"
                defaultValue="<!DOCTYPE html>&#10;<html lang='pt-BR'>&#10;<head>&#10;  <meta charset='UTF-8'>&#10;  <title>Meu Site</title>&#10;</head>&#10;<body>&#10;  <h1>Olá Mundo!</h1>&#10;</body>&#10;</html>"
              />
            </div>
          )}

          {activeTab === 'prompt' && (
            <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 self-start max-w-[85%]">
                Olá! Como posso ajudar a modificar seu código hoje?
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Rodapé Fixo: Caixa de Prompt + Navegação por Abas */}
      <footer className="bg-slate-900 border-t border-slate-800 z-10">
        {/* Barra de Entrada de Comando / IA */}
        <div className="p-2.5 flex gap-2 items-center border-b border-slate-800/60">
          <input 
            type="text" 
            value={promptText}
            onChange={(e) => setPromptText(e.target.value)}
            placeholder="O que você deseja criar ou alterar?" 
            className="flex-1 bg-slate-800 px-3.5 py-2.5 rounded-xl text-xs text-slate-100 placeholder-slate-500 border border-slate-700/60 focus:outline-none focus:border-indigo-500"
          />
          <button className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-xl text-xs font-semibold transition">
            Enviar
          </button>
        </div>

        {/* Menu de Abas Inferiores (Mobile Bottom Nav) */}
        <nav className="flex justify-around items-center py-2 text-xs">
          <button 
            onClick={() => setActiveTab('files')} 
            className={`flex flex-col items-center gap-0.5 transition ${activeTab === 'files' ? 'text-indigo-400 font-bold' : 'text-slate-400'}`}
          >
            <span className="text-base">📁</span>
            <span>Arquivos</span>
          </button>
          <button 
            onClick={() => setActiveTab('editor')} 
            className={`flex flex-col items-center gap-0.5 transition ${activeTab === 'editor' ? 'text-indigo-400 font-bold' : 'text-slate-400'}`}
          >
            <span className="text-base">📝</span>
            <span>Editor</span>
          </button>
          <button 
            onClick={() => setActiveTab('prompt')} 
            className={`flex flex-col items-center gap-0.5 transition ${activeTab === 'prompt' + '' ? 'text-indigo-400 font-bold' : 'text-slate-400'}`}
          >
            <span className="text-base">🤖</span>
            <span>Prompt IA</span>
          </button>
        </nav>
      </footer>
    </div>
  );
}
