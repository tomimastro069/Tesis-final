import React, { useState } from 'react';
import { Rnd } from 'react-rnd';
import { useWindows } from '../context/WindowsContext';

interface WindowFrameProps {
  id: string;
  defaultWidth?: number | string;
  defaultHeight?: number | string;
  defaultX?: number;
  defaultY?: number;
}

export function WindowFrame({ 
  id, 
  defaultWidth = 900, 
  defaultHeight = 600,
  defaultX = 100,
  defaultY = 100
}: WindowFrameProps) {
  const { windows, closeWindow, minimizeWindow, maximizeWindow, restoreWindow, focusWindow } = useWindows();
  
  const windowData = windows.find(w => w.id === id);
  const [size, setSize] = useState({ width: defaultWidth, height: defaultHeight });
  const [position, setPosition] = useState({ x: defaultX, y: defaultY });
  const [prevSize, setPrevSize] = useState({ width: defaultWidth, height: defaultHeight });
  const [prevPosition, setPrevPosition] = useState({ x: defaultX, y: defaultY });

  if (!windowData) return null;

  const { title, icon, component, isMinimized, isMaximized, zIndex } = windowData;

  const handleMaximizeToggle = () => {
    if (isMaximized) {
      restoreWindow(id);
      setSize(prevSize);
      setPosition(prevPosition);
    } else {
      setPrevSize(size);
      setPrevPosition(position);
      maximizeWindow(id);
      // Usar 100% del ancho y el alto, ya que el contenedor padre excluye la barra de tareas
      setSize({ width: '100%', height: '100%' } as any);
      setPosition({ x: 0, y: 0 });
    }
  };

  if (isMinimized) return null;

  return (
    <Rnd
      size={{ width: size.width, height: size.height }}
      position={{ x: position.x, y: position.y }}
      onDragStop={(e, d) => {
        if (!isMaximized) {
          setPosition({ x: d.x, y: d.y });
        }
      }}
      onResizeStop={(e, direction, ref, delta, position) => {
        if (!isMaximized) {
          setSize({ width: ref.style.width, height: ref.style.height });
          setPosition(position);
        }
      }}
      disableDragging={isMaximized}
      enableResizing={!isMaximized}
      minWidth={200}
      minHeight={150}
      bounds="parent"
      dragHandleClassName="win-title-bar"
      onMouseDown={() => focusWindow(id)}
      style={{ zIndex, pointerEvents: 'auto' }}
    >
      <div className="w-full h-full flex flex-col bg-[#c0c0c0] win98-border font-win98 pointer-events-auto overflow-hidden">
        {/* Title Bar */}
        <div 
          className="win-title-bar flex justify-between items-center text-white font-bold cursor-default select-none bg-gradient-to-r from-[#000080] to-[#1084d0] px-1 py-[2px] flex-shrink-0"
          onDoubleClick={handleMaximizeToggle}
        >
          <div className="flex items-center">
            {icon && (
              typeof icon === 'string' 
                ? <img src={icon} alt="" className="w-4 h-4 mr-1" />
                : <span className="mr-1">{icon}</span>
            )}
            <span className="text-xs">{title}</span>
          </div>
          
          {/* Buttons */}
          <div className="flex gap-[2px]">
            <button 
              onClick={(e) => { e.stopPropagation(); minimizeWindow(id); }}
              className="w-4 h-[14px] flex justify-center items-center bg-[#c0c0c0] win98-border active:win98-border-inset text-[9px] cursor-pointer outline-none font-bold"
            >
              _
            </button>
            <button 
              onClick={(e) => { e.stopPropagation(); handleMaximizeToggle(); }}
              className="w-4 h-[14px] flex justify-center items-center bg-[#c0c0c0] win98-border active:win98-border-inset text-[9px] cursor-pointer outline-none font-bold"
            >
              {isMaximized ? '❐' : '□'}
            </button>
            <button 
              onClick={(e) => { e.stopPropagation(); closeWindow(id); }}
              className="w-4 h-[14px] flex justify-center items-center bg-[#c0c0c0] win98-border active:win98-border-inset text-[9px] cursor-pointer outline-none font-bold"
            >
              X
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 min-h-0 bg-white m-[2px] win98-border-deep overflow-auto text-black flex flex-col">
          {component}
        </div>
      </div>
    </Rnd>
  );
}
