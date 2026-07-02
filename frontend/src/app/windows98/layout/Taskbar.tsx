import React, { useState, useEffect, useRef } from 'react';
import { useWindows } from '../context/WindowsContext';
import { StartMenu } from '../components/StartMenu';
import { ScanForm } from '../../components/ScanForm';
import { MSDOSPrompt } from '../components/MSDOSPrompt';
import { ReportsExplorer } from '../components/ReportsExplorer';
import AboutProject from '../components/AboutProject';

export function Taskbar() {
  const { windows, focusWindow, minimizeWindow, restoreWindow, openWindow } = useWindows();
  const [time, setTime] = useState(new Date());
  const [isStartOpen, setIsStartOpen] = useState(false);
  const startButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    
    // Cerrar menú inicio al hacer click afuera
    const handleClickOutside = (e: MouseEvent) => {
      if (startButtonRef.current && !startButtonRef.current.contains(e.target as Node)) {
        // Necesitamos ignorar los clicks dentro del propio StartMenu (idealmente a través de event.stopPropagation en el menú, o chequeando el target)
        // Por ahora lo simplificamos
        setIsStartOpen(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    
    return () => {
      clearInterval(timer);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 h-[45px] bg-[#c0c0c0] border-t border-[#dfdfdf] shadow-[inset_0_1px_0_#fff] flex items-center p-[2px] font-win98 text-sm z-[9999]">
      {/* Start Button */}
      <button 
        ref={startButtonRef}
        onClick={() => setIsStartOpen(!isStartOpen)}
        className={`font-bold py-[2px] px-2 mr-2.5 flex items-center h-full bg-[#c0c0c0] outline-none cursor-pointer ${isStartOpen ? 'win98-border-inset' : 'win98-border active:win98-border-inset'}`}
      >
        <img 
          src="https://win98icons.alexmeub.com/icons/png/windows-0.png" 
          alt="Start" 
          className="w-6 h-6 mr-1"
        />
        Start
      </button>

      {/* Menú de Inicio (Renderizado fuera del flujo normal pero posicionado) */}
      {isStartOpen && (
        <div onMouseDown={(e) => e.stopPropagation()}>
          <StartMenu 
            onClose={() => setIsStartOpen(false)} 
            items={[
              {
                label: 'Acerca del Proyecto',
                icon: 'https://win98icons.alexmeub.com/icons/png/help_book_big-0.png',
                onClick: () => openWindow({
                  id: 'about',
                  title: 'Acerca del Proyecto',
                  icon: 'https://win98icons.alexmeub.com/icons/png/help_book_big-0.png',
                  component: <AboutProject />
                })
              },
              {
                label: 'Programas',
                icon: 'https://win98icons.alexmeub.com/icons/png/directory_program_group-1.png',
                subItems: [
                  { 
                    label: 'Analizador de Seguridad', 
                    icon: 'https://win98icons.alexmeub.com/icons/png/key_padlock-0.png',
                    onClick: () => openWindow({
                      id: 'scanner',
                      title: 'Analizador de Seguridad',
                      icon: 'https://win98icons.alexmeub.com/icons/png/key_padlock-0.png',
                      component: <ScanForm onScanStarted={() => {
                        openWindow({
                          id: 'msdos',
                          title: 'MS-DOS Prompt',
                          icon: 'https://win98icons.alexmeub.com/icons/png/console_prompt-0.png',
                          component: <MSDOSPrompt />
                        });
                      }} />
                    })
                  },
                  { 
                    label: 'Explorador de Reportes', 
                    icon: 'https://win98icons.alexmeub.com/icons/png/briefcase-2.png',
                    onClick: () => openWindow({
                      id: 'reports-explorer',
                      title: 'Explorador de Reportes',
                      icon: 'https://win98icons.alexmeub.com/icons/png/briefcase-2.png',
                      component: <ReportsExplorer />
                    })
                  },
                  { 
                    label: 'MS-DOS Prompt', 
                    icon: 'https://win98icons.alexmeub.com/icons/png/console_prompt-0.png',
                    onClick: () => openWindow({
                      id: 'msdos',
                      title: 'MS-DOS Prompt',
                      icon: 'https://win98icons.alexmeub.com/icons/png/console_prompt-0.png',
                      component: <MSDOSPrompt />
                    })
                  }
                ]
              },
              {
                label: 'Apagar...',
                icon: 'https://win98icons.alexmeub.com/icons/png/shut_down_normal-1.png',
                onClick: () => alert('El sistema se apagará ahora.')
              }
            ]}
          />
        </div>
      )}

      {/* Window Tasks */}
      <div className="flex-1 flex overflow-x-hidden gap-1 h-full">
        {windows.map(win => {
          const isFocused = !win.isMinimized && win.zIndex === Math.max(...windows.map(w => w.zIndex), 0);
          return (
            <button
              key={win.id}
              onClick={() => {
                if (win.isMinimized) {
                  restoreWindow(win.id);
                } else if (isFocused) {
                  minimizeWindow(win.id);
                } else {
                  focusWindow(win.id);
                }
              }}
              className={`flex items-center px-2 h-full min-w-[100px] max-w-[150px] whitespace-nowrap overflow-hidden text-ellipsis bg-[#c0c0c0] outline-none cursor-pointer ${isFocused ? 'font-bold win98-border-inset' : 'font-normal win98-border active:win98-border-inset'}`}
            >
              {typeof win.icon === 'string' ? (
                <img src={win.icon} alt="" className="w-6 h-6 mr-2" />
              ) : win.icon}
              {win.title}
            </button>
          );
        })}
      </div>

      {/* System Tray */}
      <div className="px-2 py-[2px] h-full flex items-center shadow-[inset_1px_1px_#808080,inset_-1px_-1px_#fff] ml-1">
        {formatTime(time)}
      </div>
    </div>
  );
}
