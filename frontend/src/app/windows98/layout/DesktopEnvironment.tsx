import React, { useState } from 'react';
import { Taskbar } from './Taskbar';
import { WindowsProvider, useWindows } from '../context/WindowsContext';
import { ScanProvider } from '../context/ScanContext';
import { WindowFrame } from '../components/WindowFrame';
import { DesktopIcon } from '../components/DesktopIcon';
import { ResponsiveGridLayout } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

// Componentes del sistema
import { ScanForm } from '../../components/ScanForm';
import { MSDOSPrompt } from '../components/MSDOSPrompt';
import { ReportsExplorer } from '../components/ReportsExplorer';
import AboutProject from '../components/AboutProject';

function DesktopContent() {
  const { windows, openWindow } = useWindows();
  
  const [layouts, setLayouts] = useState<any>({
    lg: [
      { i: 'mi-pc', x: 0, y: 0, w: 1, h: 1, isResizable: false },
      { i: 'analizador', x: 0, y: 1, w: 1, h: 1, isResizable: false },
      { i: 'reportes', x: 0, y: 2, w: 1, h: 1, isResizable: false },
      { i: 'msdos-icon', x: 0, y: 3, w: 1, h: 1, isResizable: false }
    ]
  });

  return (
    <div className="w-screen h-screen bg-[#008080] relative overflow-hidden font-win98 text-white select-none">
      {/* Grilla para Iconos del Escritorio */}
      <div className="absolute top-0 bottom-[45px] left-0 right-0 z-0">
        <ResponsiveGridLayout
          className="layout"
          width={window.innerWidth}
          layouts={layouts}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={100}
          onLayoutChange={(currentLayout, allLayouts) => setLayouts(allLayouts)}
          margin={[15, 15]}
        >
          <div key="mi-pc">
            <DesktopIcon 
              label="Acerca del Proyecto"
              icon="https://win98icons.alexmeub.com/icons/png/help_book_big-0.png"
              onDoubleClick={() => {
                openWindow({
                  id: 'about',
                  title: 'Acerca del Proyecto',
                  icon: 'https://win98icons.alexmeub.com/icons/png/help_book_big-0.png',
                  component: <AboutProject />
                });
              }}
            />
          </div>
          <div key="analizador">
            <DesktopIcon 
              label="Analizador de Seguridad"
              icon="https://win98icons.alexmeub.com/icons/png/key_padlock-0.png"
              onDoubleClick={() => {
                openWindow({
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
                });
              }}
            />
          </div>
          <div key="reportes">
            <DesktopIcon 
              label="Reportes"
              icon="https://win98icons.alexmeub.com/icons/png/briefcase-2.png"
              onDoubleClick={() => {
                openWindow({
                  id: 'reports-explorer',
                  title: 'Explorador de Reportes',
                  icon: 'https://win98icons.alexmeub.com/icons/png/briefcase-2.png',
                  component: <ReportsExplorer />
                });
              }}
            />
          </div>
          <div key="msdos-icon">
            <DesktopIcon 
              label="MS-DOS Prompt"
              icon="https://win98icons.alexmeub.com/icons/png/console_prompt-0.png"
              onDoubleClick={() => {
                openWindow({
                  id: 'msdos',
                  title: 'MS-DOS Prompt',
                  icon: 'https://win98icons.alexmeub.com/icons/png/console_prompt-0.png',
                  component: <MSDOSPrompt />
                });
              }}
            />
          </div>
        </ResponsiveGridLayout>
      </div>

      {/* Ventanas Activas */}
      <div className="absolute top-0 bottom-[45px] left-0 right-0 z-10 pointer-events-none">
        {windows.map(win => (
          <WindowFrame key={win.id} id={win.id} />
        ))}
      </div>

      <Taskbar />
    </div>
  );
}

export function DesktopEnvironment() {
  return (
    <WindowsProvider>
      <ScanProvider>
        <DesktopContent />
      </ScanProvider>
    </WindowsProvider>
  );
}
