import React, { useState, useEffect, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

function App() {
  const [files, setFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [code, setCode] = useState('// Selecione um arquivo');
  const terminalRef = useRef(null);
  const termInstance = useRef(null);

  // Inicializa o Terminal
  useEffect(() => {
    termInstance.current = new Terminal({ cursorBlink: true, fontSize: 12 });
    termInstance.current.open(terminalRef.current);
    termInstance.current.writeln('Bem-vindo ao SiteForge IDE...');
  }, []);

  // Busca arquivos do seu backend Python
  useEffect(() => {
    fetch('/api/files').then(res => res.json()).then(setFiles);
  }, []);

  const handleFileClick = async (fileName) => {
    const res = await fetch(`/api/file-content?path=${fileName}`);
    const data = await res.json();
    setActiveFile(fileName);
    setCode(data.content);
  };

  const saveFile = async () => {
    await fetch('/api/file-content', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ path: activeFile, content: code })
    });
    alert('Salvo!');
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-4">
        <h2 className="text-sm font-bold text-slate-400 uppercase mb-4">Arquivos</h2>
        {files.map(f => (
          <div key={f} onClick={() => handleFileClick(f)} className="cursor-pointer hover:text-blue-400 py-1">{f}</div>
        ))}
      </aside>

      {/* Main Area */}
      <main className="flex-1 flex flex-col">
        <header className="h-12 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-4">
          <span>{activeFile || 'Nenhum arquivo'}</span>
          <button onClick={saveFile} className="bg-blue-600 px-3 py-1 rounded text-xs">Salvar</button>
        </header>
        
        <Editor
          height="70%"
          theme="vs-dark"
          path={activeFile}
          value={code}
          onChange={setCode}
        />

        <div className="flex-1 bg-slate-900 p-2 overflow-hidden">
          <div ref={terminalRef} className="h-full"></div>
        </div>
      </main>
    </div>
  );
}

export default App;
