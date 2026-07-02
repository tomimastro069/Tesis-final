import React, { useState } from 'react';
import { useWindows } from '../context/WindowsContext';
import { aboutProjectData } from '../data/aboutProjectData';

export default function AboutProject() {
  const { closeWindow } = useWindows();
  const [activeTab, setActiveTab] = useState(aboutProjectData[0].id);

  // Colores para los bordes izquierdos de los botones del menú (estilo Welcome to Windows 98)
  const tabColors = ['bg-[#00a2e8]', 'bg-[#ed1c24]', 'bg-[#22b14c]', 'bg-[#ffc90e]'];

  const activeContent = aboutProjectData.find(tab => tab.id === activeTab);

  return (
    <div className="flex flex-col h-full bg-white font-[Arial] select-none">
      {/* Banner Superior Estilo "Welcome to Windows 98" */}
      <div className="relative h-24 bg-gradient-to-b from-[#000080] via-[#3a6ea5] to-[#c0c0c0] flex items-center px-6 overflow-hidden border-b-2 border-[#808080]">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-white to-transparent opacity-50"></div>
        <h1 className="text-white text-3xl font-bold tracking-wider z-10" style={{ textShadow: '2px 2px 0px #000' }}>
          Acerca del Proyecto
        </h1>
        {/* Decoración abstracta estilo 90s */}
        <div className="absolute right-[-20px] top-[-20px] w-48 h-48 rounded-full border-4 border-white opacity-10"></div>
        <div className="absolute right-10 top-10 w-24 h-24 rounded-full border-2 border-white opacity-20"></div>
      </div>

      {/* Cuerpo Principal */}
      <div className="flex flex-1 min-h-0 bg-[#e6e6e6]">
        {/* Barra Lateral Izquierda (Navegación) */}
        <div className="w-1/3 min-w-[200px] bg-[#f0f0f0] border-r-2 border-[#808080] flex flex-col">
          <div className="bg-black text-white text-sm tracking-[0.3em] font-bold py-1 px-4 mb-2">
            C O N T E N T S
          </div>
          
          <div className="flex flex-col">
            {aboutProjectData.map((tab, index) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative flex items-center px-4 py-3 text-left border-b border-[#c0c0c0] hover:bg-[#dfdfdf] active:bg-[#c0c0c0] transition-colors ${
                    isActive ? 'font-bold bg-[#dfdfdf]' : ''
                  }`}
                >
                  {/* Borde de color a la izquierda (como en Win98) */}
                  <div className={`absolute left-0 top-0 bottom-0 w-1 ${tabColors[index % tabColors.length]}`}></div>
                  
                  <span className="ml-2 text-black text-lg">{tab.title}</span>
                  
                  {isActive && (
                    <span className="absolute right-4 text-black text-xl leading-none">
                      ✓
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Área de Contenido Derecha */}
        <div className="flex-1 p-8 overflow-y-auto bg-white flex flex-col shadow-inner">
          {activeContent && (
            <div className="max-w-xl">
              <h2 className="text-3xl font-bold mb-6 text-black border-b border-gray-300 pb-2">
                {activeContent.heading}
              </h2>
              <div className="space-y-4 text-black text-lg leading-relaxed">
                {activeContent.content.map((paragraph, idx) => (
                  <p key={idx}>{paragraph}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Pie de Página */}
      <div className="h-12 bg-[#c0c0c0] border-t-2 border-white win98-border flex items-center justify-between px-4 font-win98">
        <div className="flex items-center">
          <input type="checkbox" id="showStartup" className="mr-2" defaultChecked />
          <label htmlFor="showStartup" className="text-black text-sm cursor-pointer">
            <span className="underline">S</span>how this screen each time Windows 98 starts.
          </label>
        </div>
        
        <button 
          onClick={() => closeWindow('about')}
          className="win98-button px-6 py-1 min-w-[80px]"
        >
          Close
        </button>
      </div>
    </div>
  );
}
